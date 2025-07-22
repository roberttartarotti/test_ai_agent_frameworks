"""Human-like weather agent with MongoDB temperature tools using LangGraph."""

import logging
from typing import Dict, List, Optional, TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from common.common import ChatbotInterface, ClimateDataService
from common.common.mongodb.tools import TemperatureTools
from .config import Config


class WeatherState(TypedDict):
    """State for the weather query workflow."""
    user_query: str
    weather_data: Optional[str]
    response: Optional[str]
    messages: List[HumanMessage]


class HumanWeatherAgent:
    """A human-like weather agent that communicates naturally and uses temperature tools."""

    def __init__(self):
        """Initialize the human weather agent."""
        self.config = Config()
        self.chatbot = ChatbotInterface(response_delay=0.3, log_level="INFO")
        self.logger = self._setup_logger()
        self.temperature_tools = TemperatureTools()
        self.llm = self._setup_llm()
        self.graph = self._setup_graph()

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

    def _setup_llm(self) -> ChatOpenAI:
        """Set up the language model for the agent."""
        return ChatOpenAI(
            api_key=self.config.openai_api_key,
            temperature=self.config.openai_temperature,
            model=self.config.openai_model
        )

    def get_weather_data(self, state: WeatherState) -> WeatherState:
        """Get weather data based on user query."""
        self.logger.info(f"Getting weather data for query: {state['user_query']}")
        
        query_lower = state['user_query'].lower()
        weather_data = ""
        
        if "temperature" in query_lower and "city" in query_lower:
            # Extract city name and get temperature
            words = state['user_query'].split()
            for i, word in enumerate(words):
                if word.lower() in ["temperature", "temp", "weather"]:
                    if i + 1 < len(words):
                        city = words[i + 1]
                        try:
                            temp_data = self.temperature_tools.get_current_temperature(city)
                            weather_data = f"Current temperature for {city}: {temp_data}"
                        except:
                            weather_data = f"Temperature data for {city} not available"
                        break
        
        elif "compare" in query_lower or "between" in query_lower:
            # Try to extract two cities for comparison
            words = state['user_query'].split()
            cities = []
            for word in words:
                if word[0].isupper() and len(word) > 2:  # Simple city detection
                    cities.append(word)
            if len(cities) >= 2:
                try:
                    comparison = self.temperature_tools.get_temperature_comparison(f"{cities[0]},{cities[1]}")
                    weather_data = f"Temperature comparison: {comparison}"
                except:
                    weather_data = f"Comparison data for {cities[0]} and {cities[1]} not available"
        
        elif "summary" in query_lower or "all" in query_lower:
            try:
                summary = self.temperature_tools.get_weather_summary()
                weather_data = f"Weather summary: {summary}"
            except:
                weather_data = "Weather summary not available"
        
        else:
            try:
                all_temps = self.temperature_tools.get_all_cities_temperatures()
                weather_data = f"All cities temperatures: {all_temps}"
            except:
                weather_data = "Temperature data not available"
        
        return {
            **state,
            "weather_data": weather_data
        }

    def generate_response(self, state: WeatherState) -> WeatherState:
        """Generate a friendly response based on weather data."""
        self.logger.info("Generating weather response")
        
        response_prompt = f"""You are a friendly and knowledgeable weather expert who loves helping people 
        understand weather conditions around the world. You communicate in a 
        warm, conversational manner and always try to make weather information interesting and 
        accessible.

        The user asked: "{state['user_query']}"

        Available weather data: {state['weather_data']}

        Please help them with their weather-related question. Respond in a friendly, 
        conversational manner. Make the weather information interesting and easy to understand.
        
        Always be helpful, friendly, and conversational in your response."""
        
        messages = [HumanMessage(content=response_prompt)]
        response = self.llm.invoke(messages)
        
        return {
            **state,
            "response": response.content,
            "messages": state["messages"] + [response]
        }

    def _setup_graph(self) -> StateGraph:
        """Set up the LangGraph workflow."""
        workflow = StateGraph(WeatherState)
        
        # Add nodes
        workflow.add_node("get_data", self.get_weather_data)
        workflow.add_node("generate_response", self.generate_response)
        
        # Set entry point
        workflow.set_entry_point("get_data")
        
        # Define the flow
        workflow.add_edge("get_data", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()

    def process_weather_query(self, user_query: str) -> str:
        """Process a weather query and return a response."""
        self.logger.info(f"Processing weather query: {user_query}")
        
        # Initialize state
        initial_state = WeatherState(
            user_query=user_query,
            weather_data=None,
            response=None,
            messages=[]
        )
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        self.logger.info(f"Generated response: {result['response']}")
        return result['response']

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