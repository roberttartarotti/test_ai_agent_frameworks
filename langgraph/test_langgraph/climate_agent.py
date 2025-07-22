"""LangGraph climate agent for city climate information."""

import logging
import sys
import os
from typing import Dict, List, Optional, TypedDict, Annotated

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from common.common import ChatbotInterface, ClimateDataService
from .config import Config


class ClimateState(TypedDict):
    """State for the climate analysis workflow."""
    city_name: str
    research_data: Optional[str]
    analysis_data: Optional[str]
    advice_data: Optional[str]
    messages: List[HumanMessage]


class ClimateAgent:
    """LangGraph agent for providing climate information about cities."""

    def __init__(self):
        """Initialize the climate agent with configuration and services."""
        self.config = Config()
        self.chatbot = ChatbotInterface(response_delay=0.5, log_level="INFO")
        self.logger = self._setup_logger()
        
        self.climate_service = ClimateDataService()
        self.llm = self._setup_llm()
        self.graph = self._setup_graph()

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

    def climate_researcher(self, state: ClimateState) -> ClimateState:
        """Climate researcher node that gathers comprehensive climate data."""
        self.logger.info(f"Researching climate data for {state['city_name']}")
        
        research_prompt = f"""You are an expert climate researcher with years of experience 
        analyzing weather patterns, temperature data, and climate trends for cities 
        around the world. You have access to comprehensive climate databases and 
        can provide detailed information about temperature, precipitation, humidity, 
        and seasonal patterns.

        Research comprehensive climate information for {state['city_name']}. 
        Gather data about:
        - Average temperatures (monthly and yearly)
        - Precipitation patterns
        - Humidity levels
        - Seasonal variations
        - Climate classification
        - Any notable climate events or trends

        Provide a detailed climate research report for {state['city_name']}."""
        
        messages = [HumanMessage(content=research_prompt)]
        response = self.llm.invoke(messages)
        
        return {
            **state,
            "research_data": response.content,
            "messages": state["messages"] + [response]
        }

    def climate_analyst(self, state: ClimateState) -> ClimateState:
        """Climate analyst node that analyzes the research data."""
        self.logger.info(f"Analyzing climate data for {state['city_name']}")
        
        analysis_prompt = f"""You are a skilled climate analyst who specializes in 
        interpreting climate data and providing actionable insights. You can 
        identify patterns, trends, and anomalies in climate data, and offer 
        recommendations based on historical and current climate information.

        Analyze the climate data for {state['city_name']} and provide insights:
        - Identify key climate patterns and trends
        - Compare with historical data if available
        - Highlight any unusual or notable climate characteristics
        - Assess climate suitability for different activities
        - Provide climate-related recommendations

        Research data: {state['research_data']}

        Focus on practical insights that would be useful for residents and visitors.
        Provide climate analysis and insights for {state['city_name']}."""
        
        messages = [HumanMessage(content=analysis_prompt)]
        response = self.llm.invoke(messages)
        
        return {
            **state,
            "analysis_data": response.content,
            "messages": state["messages"] + [response]
        }

    def climate_advisor(self, state: ClimateState) -> ClimateState:
        """Climate advisor node that provides user-friendly advice."""
        self.logger.info(f"Generating advice for {state['city_name']}")
        
        advice_prompt = f"""You are a friendly climate advisor who helps people 
        understand climate information in simple terms. You can explain complex 
        climate data in an accessible way and provide practical advice for 
        different activities based on climate conditions.

        Based on the climate research and analysis for {state['city_name']}, 
        provide user-friendly advice and recommendations:
        - Best times to visit or engage in outdoor activities
        - What to pack or prepare for different seasons
        - Climate considerations for daily life
        - Weather-related tips and precautions
        - Seasonal highlights and attractions

        Analysis data: {state['analysis_data']}

        Make the information accessible and practical for everyday use.
        Provide practical climate advice for {state['city_name']}."""
        
        messages = [HumanMessage(content=advice_prompt)]
        response = self.llm.invoke(messages)
        
        return {
            **state,
            "advice_data": response.content,
            "messages": state["messages"] + [response]
        }

    def _setup_graph(self) -> StateGraph:
        """Set up the LangGraph workflow."""
        workflow = StateGraph(ClimateState)
        
        workflow.add_node("researcher", self.climate_researcher)
        workflow.add_node("analyst", self.climate_analyst)
        workflow.add_node("advisor", self.climate_advisor)
        
        workflow.set_entry_point("researcher")
        
        workflow.add_edge("researcher", "analyst")
        workflow.add_edge("analyst", "advisor")
        workflow.add_edge("advisor", END)
        
        return workflow.compile()

    def get_climate_info(self, city_name: str) -> Dict:
        """Get comprehensive climate information for a city.

        Args:
            city_name: Name of the city to get climate information for.

        Returns:
            Dictionary containing climate information and recommendations.
        """
        self.logger.info(f"Starting climate analysis for {city_name}")
        
        initial_state = ClimateState(
            city_name=city_name,
            research_data=None,
            analysis_data=None,
            advice_data=None,
            messages=[]
        )
        
        result = self.graph.invoke(initial_state)
        
        climate_data = {
            "city": city_name,
            "research": result["research_data"],
            "analysis": result["analysis_data"],
            "advice": result["advice_data"],
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