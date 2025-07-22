"""Human-like weather agent with MongoDB temperature tools."""

import logging
from typing import Dict, List

from crewai import Agent, Task, Crew, Process

from common.common import ChatbotInterface, ClimateDataService
from common.common.mongodb.tools import TemperatureTools
from .config import Config


class HumanWeatherAgent:
    """A human-like weather agent that communicates naturally and uses temperature tools."""

    def __init__(self):
        """Initialize the human weather agent."""
        self.config = Config()
        self.chatbot = ChatbotInterface(response_delay=0.3, log_level="INFO")
        self.logger = self._setup_logger()
        self.temperature_tools = TemperatureTools()

    def _setup_logger(self) -> logging.Logger:
        """Set up logger for the weather agent."""
        logger = logging.getLogger("human_weather_agent")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def create_weather_expert_agent(self) -> Agent:
        """Create a weather expert agent."""
        return Agent(
            role="Weather Expert",
            goal="Provide accurate and friendly weather information",
            backstory="""You are a friendly and knowledgeable weather expert who loves helping people 
            understand weather conditions around the world. You communicate in a 
            warm, conversational manner and always try to make weather information interesting and 
            accessible.""",
            verbose=True,
            allow_delegation=False,
            llm=self.config.get_llm_config()
        )

    def create_weather_conversation_task(self, user_query: str) -> Task:
        """Create a task for weather conversation."""
        return Task(
            description=f"""The user asked: "{user_query}"
            
            Please help them with their weather-related question. Use the available tools to get 
            accurate information and respond in a friendly, conversational manner. 
            
            If they're asking about:
            - A specific city's temperature: Use get_current_temperature
            - Comparing cities: Use get_temperature_comparison
            - General weather info: Use get_weather_summary or get_all_cities_temperatures
            - Updating data: Use update_city_temperature
            
            Always be helpful, friendly, and conversational in your response. Make the weather 
            information interesting and easy to understand.""",
            agent=self.create_weather_expert_agent(),
            expected_output="A friendly, conversational response with accurate weather information"
        )

    def process_weather_query(self, user_query: str) -> str:
        """Process a weather query and return a response."""
        self.logger.info(f"Processing weather query: {user_query}")
        
        crew = Crew(
            agents=[self.create_weather_expert_agent()],
            tasks=[self.create_weather_conversation_task(user_query)],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        response = result[0] if result else "I'm sorry, I couldn't process your weather query right now."
        
        self.logger.info(f"Generated response: {response}")
        return response

    def start_interactive_mode(self) -> None:
        """Start the weather agent in interactive mode."""
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