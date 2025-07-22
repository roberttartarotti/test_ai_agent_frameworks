"""Main entry point for the CrewAI agents."""

import logging
import sys
from typing import Optional

from .climate_agent import ClimateAgent
from .human_weather_agent import HumanWeatherAgent
from .config import Config


def setup_logging() -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )


def validate_environment() -> bool:
    """Validate that required environment variables are set.

    Returns:
        True if environment is valid, False otherwise.
    """
    try:
        config = Config()
        return config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        return False


def main(city_name: Optional[str] = None, agent_type: str = "weather") -> None:
    """Main function to run the agents.

    Args:
        city_name: Optional city name to analyze climate for.
        agent_type: Type of agent to run ("weather" or "climate").
    """
    setup_logging()
    logger = logging.getLogger("main")
    
    if not validate_environment():
        logger.error("Environment validation failed. Please check your configuration.")
        sys.exit(1)
    
    try:
        if agent_type == "weather":
            weather_agent = HumanWeatherAgent()
            logger.info("Starting human weather agent")
            weather_agent.start_interactive_mode()
            weather_agent.close()
        else:
            climate_agent = ClimateAgent()
            
            if city_name:
                logger.info(f"Analyzing climate for {city_name}")
                climate_info = climate_agent.get_climate_info(city_name)
                print(f"\nClimate Information for {city_name}:")
                print("=" * 50)
                print(f"Research: {climate_info['research']}")
                print(f"Analysis: {climate_info['analysis']}")
                print(f"Advice: {climate_info['advice']}")
            else:
                logger.info("Starting interactive mode")
                climate_agent.start_interactive_mode()
            
            climate_agent.close()
            
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CrewAI Agents")
    parser.add_argument(
        "--city", 
        type=str, 
        help="City name to analyze climate for"
    )
    parser.add_argument(
        "--agent",
        type=str,
        choices=["weather", "climate"],
        default="weather",
        help="Type of agent to run (weather or climate)"
    )
    
    args = parser.parse_args()
    main(args.city, args.agent) 