"""Human-like weather agent with MongoDB temperature tools using Agno."""

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
from common.common.mongodb.tools import TemperatureTools
from common.common.logging_config import get_logger
from test_agno.config import Config


class HumanWeatherAgent:
    """A human-like weather agent that communicates naturally and uses temperature tools."""

    def __init__(self):
        """Initialize the human weather agent with configuration and tools."""
        self.config = Config()
        self.chatbot = ChatbotInterface(response_delay=0.3, log_level="INFO")
        self.logger = get_logger("human_weather_agent")
        self.temperature_tools = TemperatureTools()
        self.openai_client = self._setup_openai_client()
        self.weather_agent = self._setup_weather_agent()

    def _setup_openai_client(self) -> OpenAI:
        """Set up OpenAI client.

        Returns:
            Configured OpenAI client
        """
        self.logger.debug("Setting up OpenAI client")
        return OpenAI(api_key=self.config.openai_api_key)

    def _setup_weather_agent(self) -> Agent:
        """Set up weather expert agent.

        Returns:
            Configured weather agent
        """
        self.logger.info("Setting up weather expert agent")
        
        model = OpenAIChat(
            id=self.config.openai_model,
            temperature=self.config.openai_temperature,
            api_key=self.config.openai_api_key
        )
        
        weather_agent = Agent(
            name="Weather Expert",
            description="Friendly and knowledgeable weather expert who loves helping people understand weather conditions around the world.",
            instructions="""You are a friendly and knowledgeable weather expert who loves helping people 
            understand weather conditions around the world. You communicate in a 
            warm, conversational manner and always try to make weather information interesting and 
            accessible.

            When helping users with weather-related questions:
            - Be friendly and conversational
            - Make weather information interesting and easy to understand
            - Use the available weather data to provide accurate information
            - Always be helpful and supportive
            - Explain complex weather concepts in simple terms

            You have access to temperature data and can help with:
            - Current temperatures for cities
            - Temperature comparisons between cities
            - Weather summaries and general information
            - All cities temperature data

            Always respond in a warm, conversational manner.""",
            model=model
        )
        
        self.logger.info("Weather agent setup completed")
        return weather_agent

    def get_weather_data(self, user_query: str) -> str:
        """Get weather data based on user query.

        Args:
            user_query: User's weather query

        Returns:
            Weather data response string
        """
        query_lower = user_query.lower()
        
        if "temperature" in query_lower and "city" in query_lower:
            words = user_query.split()
            for i, word in enumerate(words):
                if word.lower() in ["temperature", "temp", "weather"]:
                    if i + 1 < len(words):
                        city = words[i + 1]
                        try:
                            temp_data = self.temperature_tools.get_current_temperature(city)
                            return f"Current temperature for {city}: {temp_data}"
                        except:
                            return f"Temperature data for {city} not available"
        
        elif "compare" in query_lower or "between" in query_lower:
            words = user_query.split()
            cities = []
            for word in words:
                if word[0].isupper() and len(word) > 2:
                    cities.append(word)
            if len(cities) >= 2:
                try:
                    comparison = self.temperature_tools.get_temperature_comparison(f"{cities[0]},{cities[1]}")
                    return f"Temperature comparison: {comparison}"
                except:
                    return f"Comparison data for {cities[0]} and {cities[1]} not available"
        
        elif "summary" in query_lower or "all" in query_lower:
            try:
                summary = self.temperature_tools.get_weather_summary()
                return f"Weather summary: {summary}"
            except:
                return "Weather summary not available"
        
        else:
            try:
                all_temps = self.temperature_tools.get_all_cities_temperatures()
                return f"All cities temperatures: {all_temps}"
            except:
                return "Temperature data not available"

    def process_weather_query(self, user_query: str) -> str:
        """Process weather query and generate response.

        Args:
            user_query: User's weather query

        Returns:
            Generated weather response
        """
        self.logger.info(f"Processing weather query: {user_query}")
        
        weather_data = self.get_weather_data(user_query)
        
        prompt = f"""The user asked: "{user_query}"

Available weather data: {weather_data}

Please help them with their weather-related question. Respond in a friendly, 
conversational manner. Make the weather information interesting and easy to understand.
        
Always be helpful, friendly, and conversational in your response."""
        
        response = self.weather_agent.run(prompt)
        
        self.logger.info(f"Generated response: {response}")
        return response

    def start_interactive_mode(self) -> None:
        """Start interactive mode for weather queries."""
        self.logger.info("Starting Human Weather Agent in interactive mode")
        self.chatbot.send_message("Hi! I'm your friendly weather assistant. I can help you with temperature information for cities around the world. What would you like to know?")
        
        while True:
            try:
                user_input = input(f"[{self.chatbot._get_timestamp()}] You: ")
                
                if user_input.lower() in ["quit", "exit", "q", "bye", "goodbye"]:
                    self.chatbot.receive_response("Thanks for chatting with me! Have a great day and stay weather-aware! 👋")
                    break
                
                if user_input.strip():
                    self.chatbot.send_message("Let me check that for you...")
                    response = self.process_weather_query(user_input)
                    self.chatbot.receive_response(response)
                else:
                    self.chatbot.receive_response("I didn't catch that. Could you please ask me about weather or temperatures for any city?")
                    
            except KeyboardInterrupt:
                self.chatbot.receive_response("Thanks for chatting! Take care! 👋")
                break
            except Exception as e:
                self.logger.error(f"Error in interactive mode: {str(e)}")
                self.chatbot.receive_response("Oops! I encountered a little weather hiccup. Could you try asking again?")

    def close(self) -> None:
        """Close the weather agent and clean up resources."""
        self.temperature_tools.close()
        self.logger.info("Human Weather Agent closed") 