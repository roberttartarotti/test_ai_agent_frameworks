"""Agno climate agent for city climate information."""

import sys
import os
from typing import Dict, List, Optional

from agno.agent import Agent, Message
from agno.models.openai import OpenAIChat
from openai import OpenAI
from typing import Dict, Any, List
import json
from pydantic import BaseModel
from agno.tools import tool

from common.common import ChatbotInterface, ClimateDataService
from common.common.logging_config import get_logger
from test_agno.config import Config


class ClimateAgent:
    """Agno agent for providing climate information about cities."""

    def __init__(self):
        """Initialize the climate agent with configuration and services."""
        self.config = Config()
        self.chatbot = ChatbotInterface(response_delay=0.5, log_level="INFO")
        self.logger = get_logger("climate_agent")
        
        self.climate_service = ClimateDataService()
        self.openai_client = self._setup_openai_client()
        self.agents = self._setup_agents()

    def _setup_openai_client(self) -> OpenAI:
        """Set up OpenAI client.

        Returns:
            Configured OpenAI client
        """
        self.logger.debug("Setting up OpenAI client")
        return OpenAI(api_key=self.config.openai_api_key)

    def _setup_agents(self) -> Dict[str, Agent]:
        """Set up Agno agents for climate analysis.

        Returns:
            Dictionary of configured agents
        """
        self.logger.info("Setting up Agno agents for climate analysis")
        
        model = OpenAIChat(
            id=self.config.openai_model,
            temperature=self.config.openai_temperature,
            api_key=self.config.openai_api_key
        )
        
        researcher_agent = Agent(
            name="Climate Researcher",
            description="Expert climate researcher with years of experience analyzing weather patterns, temperature data, and climate trends for cities around the world.",
            instructions="""You are an expert climate researcher with years of experience 
            analyzing weather patterns, temperature data, and climate trends for cities 
            around the world. You have access to comprehensive climate databases and 
            can provide detailed information about temperature, precipitation, humidity, 
            and seasonal patterns.

            When asked about a city's climate, research comprehensive climate information including:
            - Average temperatures (monthly and yearly)
            - Precipitation patterns
            - Humidity levels
            - Seasonal variations
            - Climate classification
            - Any notable climate events or trends

            Provide detailed, accurate climate research reports.""",
            model=model
        )
        
        analyst_agent = Agent(
            name="Climate Analyst",
            description="Skilled climate analyst who specializes in interpreting climate data and providing actionable insights.",
            instructions="""You are a skilled climate analyst who specializes in 
            interpreting climate data and providing actionable insights. You can 
            identify patterns, trends, and anomalies in climate data, and offer 
            recommendations based on historical and current climate information.

            When analyzing climate data, focus on:
            - Identifying key climate patterns and trends
            - Comparing with historical data if available
            - Highlighting unusual or notable climate characteristics
            - Assessing climate suitability for different activities
            - Providing climate-related recommendations

            Focus on practical insights that would be useful for residents and visitors.""",
            model=model
        )
        
        advisor_agent = Agent(
            name="Climate Advisor",
            description="Friendly climate advisor who helps people understand climate information in simple terms.",
            instructions="""You are a friendly climate advisor who helps people 
            understand climate information in simple terms. You can explain complex 
            climate data in an accessible way and provide practical advice for 
            different activities based on climate conditions.

            When providing advice, focus on:
            - Best times to visit or engage in outdoor activities
            - What to pack or prepare for different seasons
            - Climate considerations for daily life
            - Weather-related tips and precautions
            - Seasonal highlights and attractions

            Make the information accessible and practical for everyday use.""",
            model=model
        )
        
        self.logger.info("Agno agents setup completed")
        return {
            "researcher": researcher_agent,
            "analyst": analyst_agent,
            "advisor": advisor_agent
        }

    def get_climate_info(self, city_name: str) -> Dict:
        """Get comprehensive climate information for a city.

        Args:
            city_name: Name of the city to analyze

        Returns:
            Dictionary containing climate research, analysis, and advice
        """
        self.logger.info(f"Starting climate analysis for {city_name}")
        
        research_prompt = f"Research comprehensive climate information for {city_name}. Provide a detailed climate research report."
        research_result = self.agents["researcher"].run(research_prompt)
        
        analysis_prompt = f"Analyze the following climate research data for {city_name} and provide insights:\n\n{research_result}"
        analysis_result = self.agents["analyst"].run(analysis_prompt)
        
        advice_prompt = f"Based on the climate research and analysis for {city_name}, provide user-friendly advice and recommendations:\n\nResearch: {research_result}\n\nAnalysis: {analysis_result}"
        advice_result = self.agents["advisor"].run(advice_prompt)
        
        # Extract content from RunResponse objects if they are RunResponse instances
        if hasattr(research_result, 'content'):
            research_content = research_result.content
        else:
            research_content = str(research_result)
            
        if hasattr(analysis_result, 'content'):
            analysis_content = analysis_result.content
        else:
            analysis_content = str(analysis_result)
            
        if hasattr(advice_result, 'content'):
            advice_content = advice_result.content
        else:
            advice_content = str(advice_result)
        
        climate_data = {
            "city": city_name,
            "research": research_content,
            "analysis": analysis_content,
            "advice": advice_content,
            "timestamp": self.chatbot._get_timestamp()
        }
        
        self.climate_service.insert_city_climate(climate_data)
        self.logger.info(f"Completed climate analysis for {city_name}")
        
        return climate_data

    def start_interactive_mode(self) -> None:
        """Start interactive mode for climate queries."""
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
            user_input: User's input text

        Returns:
            Extracted city name or None if not found
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