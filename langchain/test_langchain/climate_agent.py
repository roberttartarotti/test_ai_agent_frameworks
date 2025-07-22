"""LangChain climate agent for city climate information."""

import logging
import sys
import os
from typing import Dict, List, Optional

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from typing import Dict, Any, List
import json
from pydantic import BaseModel
from langchain.agents import initialize_agent, AgentType

from common.common import ChatbotInterface, ClimateDataService
from common.common.logging_config import get_logger
from .config import Config

logger = get_logger("langchain_climate_agent")


class ClimateAgent:
    """LangChain agent for providing climate information about cities."""

    def __init__(self):
        """Initialize the climate agent with configuration and services."""
        self.config = Config()
        self.chatbot = ChatbotInterface(response_delay=0.5, log_level="INFO")
        self.logger = self._setup_logger()
        
        self.climate_service = ClimateDataService()
        self.llm = self._setup_llm()

    def _setup_logger(self) -> logging.Logger:
        """Set up logger for the climate agent.

        Returns:
            Configured logger instance.
        """
        logger = logging.getLogger("climate_agent")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _setup_llm(self) -> ChatOpenAI:
        """Set up the language model for the agent.

        Returns:
            Configured ChatOpenAI instance.
        """
        return ChatOpenAI(
            api_key=self.config.openai_api_key,
            temperature=self.config.openai_temperature,
            model=self.config.openai_model
        )

    def create_climate_researcher_prompt(self) -> PromptTemplate:
        """Create a prompt template for climate research."""
        return PromptTemplate(
            input_variables=["city_name"],
            template="""You are an expert climate researcher with years of experience 
            analyzing weather patterns, temperature data, and climate trends for cities 
            around the world. You have access to comprehensive climate databases and 
            can provide detailed information about temperature, precipitation, humidity, 
            and seasonal patterns.

            Research comprehensive climate information for {city_name}. 
            Gather data about:
            - Average temperatures (monthly and yearly)
            - Precipitation patterns
            - Humidity levels
            - Seasonal variations
            - Climate classification
            - Any notable climate events or trends

            Provide a detailed climate research report for {city_name}."""
        )

    def create_climate_analyst_prompt(self) -> PromptTemplate:
        """Create a prompt template for climate analysis."""
        return PromptTemplate(
            input_variables=["city_name", "research_data"],
            template="""You are a skilled climate analyst who specializes in 
            interpreting climate data and providing actionable insights. You can 
            identify patterns, trends, and anomalies in climate data, and offer 
            recommendations based on historical and current climate information.

            Analyze the climate data for {city_name} and provide insights:
            - Identify key climate patterns and trends
            - Compare with historical data if available
            - Highlight any unusual or notable climate characteristics
            - Assess climate suitability for different activities
            - Provide climate-related recommendations

            Research data: {research_data}

            Focus on practical insights that would be useful for residents and visitors.
            Provide climate analysis and insights for {city_name}."""
        )

    def create_climate_advisor_prompt(self) -> PromptTemplate:
        """Create a prompt template for climate advice."""
        return PromptTemplate(
            input_variables=["city_name", "analysis_data"],
            template="""You are a friendly climate advisor who helps people 
            understand climate information in simple terms. You can explain complex 
            climate data in an accessible way and provide practical advice for 
            different activities based on climate conditions.

            Based on the climate research and analysis for {city_name}, 
            provide user-friendly advice and recommendations:
            - Best times to visit or engage in outdoor activities
            - What to pack or prepare for different seasons
            - Climate considerations for daily life
            - Weather-related tips and precautions
            - Seasonal highlights and attractions

            Analysis data: {analysis_data}

            Make the information accessible and practical for everyday use.
            Provide practical climate advice for {city_name}."""
        )

    def get_climate_info(self, city_name: str) -> Dict:
        """Get comprehensive climate information for a city.

        Args:
            city_name: Name of the city to get climate information for.

        Returns:
            Dictionary containing climate information and recommendations.
        """
        self.logger.info(f"Starting climate analysis for {city_name}")
        
        research_chain = LLMChain(llm=self.llm, prompt=self.create_climate_researcher_prompt())
        research_result = research_chain.run(city_name=city_name)
        
        analysis_chain = LLMChain(llm=self.llm, prompt=self.create_climate_analyst_prompt())
        analysis_result = analysis_chain.run(city_name=city_name, research_data=research_result)
        
        advice_chain = LLMChain(llm=self.llm, prompt=self.create_climate_advisor_prompt())
        advice_result = advice_chain.run(city_name=city_name, analysis_data=analysis_result)
        
        climate_data = {
            "city": city_name,
            "research": research_result,
            "analysis": analysis_result,
            "advice": advice_result,
            "timestamp": self.chatbot._get_timestamp()
        }
        
        self.climate_service.insert_city_climate(climate_data)
        self.logger.info(f"Completed climate analysis for {city_name}")
        
        return climate_data

    def start_interactive_mode(self) -> None:
        """Start the climate agent in interactive mode."""
        self.logger.info("Starting Climate Agent in interactive mode")
        self.chatbot.send_message("Climate Agent started. Ask me about any city's climate!")
        
        while True:
            try:
                user_input = input(f"[{self.chatbot._get_timestamp()}] You: ")
                
                if user_input.lower() in ["quit", "exit", "q"]:
                    self.chatbot.receive_response("Goodbye! Climate Agent stopping.")
                    break
                
                if "climate" in user_input.lower() or "weather" in user_input.lower():
                    city_name = self._extract_city_name(user_input)
                    if city_name:
                        self.chatbot.send_message(f"Researching climate information for {city_name}...")
                        climate_info = self.get_climate_info(city_name)
                        self.chatbot.receive_response(f"Here's what I found about {city_name}'s climate:\n{climate_info['advice']}")
                    else:
                        self.chatbot.receive_response("Please specify a city name for climate information.")
                else:
                    self.chatbot.receive_response("I can help you with climate information for any city. Just ask about a specific city's climate!")
                    
            except KeyboardInterrupt:
                self.chatbot.receive_response("Climate Agent interrupted. Goodbye!")
                break
            except Exception as e:
                self.logger.error(f"Error in interactive mode: {str(e)}")
                self.chatbot.receive_response(f"Sorry, I encountered an error: {str(e)}")

    def _extract_city_name(self, user_input: str) -> Optional[str]:
        """Extract city name from user input.

        Args:
            user_input: User's input text.

        Returns:
            Extracted city name or None if not found.
        """
        words = user_input.split()
        for i, word in enumerate(words):
            if word.lower() in ["climate", "weather", "of", "in", "for"]:
                if i + 1 < len(words):
                    return words[i + 1].title()
        return None

    def close(self) -> None:
        """Close the climate agent and clean up resources."""
        self.climate_service.close()
        self.logger.info("Climate Agent closed") 