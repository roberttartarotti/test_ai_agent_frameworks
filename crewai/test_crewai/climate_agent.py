"""CrewAI climate agent for city climate information."""

import logging
import sys
import os
from typing import Dict, List, Optional

from crewai import Agent, Task, Crew, Process

from common.common import ChatbotInterface, ClimateDataService
from .config import Config


class ClimateAgent:
    """CrewAI agent for providing climate information about cities."""

    def __init__(self):
        """Initialize the climate agent with configuration and services."""
        self.config = Config()
        self.chatbot = ChatbotInterface(response_delay=0.5, log_level="INFO")
        self.logger = self._setup_logger()
        
        self.climate_service = ClimateDataService()

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

    def create_climate_researcher_agent(self) -> Agent:
        """Create a climate researcher agent.

        Returns:
            Configured climate researcher agent.
        """
        return Agent(
            role="Climate Researcher",
            goal="Research and provide accurate climate information for cities",
            backstory="""You are an expert climate researcher with years of experience 
            analyzing weather patterns, temperature data, and climate trends for cities 
            around the world. You have access to comprehensive climate databases and 
            can provide detailed information about temperature, precipitation, humidity, 
            and seasonal patterns.""",
            verbose=True,
            allow_delegation=False,
            llm=self.config.get_llm_config()
        )

    def create_climate_analyst_agent(self) -> Agent:
        """Create a climate analyst agent.

        Returns:
            Configured climate analyst agent.
        """
        return Agent(
            role="Climate Analyst",
            goal="Analyze climate data and provide insights and recommendations",
            backstory="""You are a skilled climate analyst who specializes in 
            interpreting climate data and providing actionable insights. You can 
            identify patterns, trends, and anomalies in climate data, and offer 
            recommendations based on historical and current climate information.""",
            verbose=True,
            allow_delegation=False,
            llm=self.config.get_llm_config()
        )

    def create_climate_advisor_agent(self) -> Agent:
        """Create a climate advisor agent.

        Returns:
            Configured climate advisor agent.
        """
        return Agent(
            role="Climate Advisor",
            goal="Provide user-friendly climate advice and recommendations",
            backstory="""You are a friendly climate advisor who helps people 
            understand climate information in simple terms. You can explain complex 
            climate data in an accessible way and provide practical advice for 
            different activities based on climate conditions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.config.get_llm_config()
        )

    def create_research_task(self, city_name: str) -> Task:
        """Create a research task for climate information.

        Args:
            city_name: Name of the city to research.

        Returns:
            Configured research task.
        """
        return Task(
            description=f"""Research comprehensive climate information for {city_name}. 
            Gather data about:
            - Average temperatures (monthly and yearly)
            - Precipitation patterns
            - Humidity levels
            - Seasonal variations
            - Climate classification
            - Any notable climate events or trends
            
            Use the climate database to retrieve existing data and supplement with 
            current information if needed.""",
            agent=self.create_climate_researcher_agent(),
            expected_output=f"Detailed climate research report for {city_name}"
        )

    def create_analysis_task(self, city_name: str) -> Task:
        """Create an analysis task for climate data.

        Args:
            city_name: Name of the city to analyze.

        Returns:
            Configured analysis task.
        """
        return Task(
            description=f"""Analyze the climate data for {city_name} and provide insights:
            - Identify key climate patterns and trends
            - Compare with historical data if available
            - Highlight any unusual or notable climate characteristics
            - Assess climate suitability for different activities
            - Provide climate-related recommendations
            
            Focus on practical insights that would be useful for residents and visitors.""",
            agent=self.create_climate_analyst_agent(),
            expected_output=f"Climate analysis and insights for {city_name}",
            context=[self.create_research_task(city_name)]
        )

    def create_advice_task(self, city_name: str) -> Task:
        """Create an advice task for climate recommendations.

        Args:
            city_name: Name of the city to provide advice for.

        Returns:
            Configured advice task.
        """
        return Task(
            description=f"""Based on the climate research and analysis for {city_name}, 
            provide user-friendly advice and recommendations:
            - Best times to visit or engage in outdoor activities
            - What to pack or prepare for different seasons
            - Climate considerations for daily life
            - Weather-related tips and precautions
            - Seasonal highlights and attractions
            
            Make the information accessible and practical for everyday use.""",
            agent=self.create_climate_advisor_agent(),
            expected_output=f"Practical climate advice for {city_name}",
            context=[self.create_analysis_task(city_name)]
        )

    def get_climate_info(self, city_name: str) -> Dict:
        """Get comprehensive climate information for a city.

        Args:
            city_name: Name of the city to get climate information for.

        Returns:
            Dictionary containing climate information and recommendations.
        """
        self.logger.info(f"Starting climate analysis for {city_name}")
        
        crew = Crew(
            agents=[
                self.create_climate_researcher_agent(),
                self.create_climate_analyst_agent(),
                self.create_climate_advisor_agent()
            ],
            tasks=[
                self.create_research_task(city_name),
                self.create_analysis_task(city_name),
                self.create_advice_task(city_name)
            ],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        
        if hasattr(result, 'final_output'):
            final_output = result.final_output
            advice = final_output
            research = final_output
            analysis = final_output
        elif hasattr(result, 'raw'):
            result_data = result.raw
            if isinstance(result_data, list) and len(result_data) >= 3:
                research = result_data[0]
                analysis = result_data[1]
                advice = result_data[2]
            else:
                advice = str(result_data)
                research = advice
                analysis = advice
        else:
            result_data = result
            if isinstance(result_data, list) and len(result_data) >= 3:
                research = result_data[0]
                analysis = result_data[1]
                advice = result_data[2]
            else:
                advice = str(result_data)
                research = advice
                analysis = advice
        
        climate_data = {
            "city": city_name,
            "research": research,
            "analysis": analysis,
            "advice": advice,
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