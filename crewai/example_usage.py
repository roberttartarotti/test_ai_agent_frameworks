"""
Example usage of the CrewAI test library.

This script demonstrates how to use the CrewAI agents for weather and climate information.
"""

import os
import sys

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_crewai.main import main


def run_examples():
    """Run example demonstrations of the CrewAI agents.
    
    This function demonstrates:
    1. Weather Agent in interactive mode
    2. Climate Agent analyzing a specific city
    3. Climate Agent in interactive mode
    """
    
    # Set up environment variables (in a real application, these would be set in your environment)
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
    os.environ["OPENAI_MODEL"] = "gpt-3.5-turbo"
    
    print("CrewAI Test Library Example")
    print("=" * 40)
    print()
    
    # Example 1: Weather Agent (Interactive Mode)
    print("1. Starting Weather Agent in Interactive Mode")
    print("   (This will start an interactive chat session)")
    print("   Type 'quit' to exit the weather agent")
    print()
    
    try:
        main(agent_type="weather")
    except KeyboardInterrupt:
        print("\nWeather agent session interrupted.")
    
    print()
    print("=" * 40)
    print()
    
    # Example 2: Climate Agent (Specific City)
    print("2. Climate Agent - Analyzing New York City")
    print()
    
    try:
        main(city_name="New York", agent_type="climate")
    except Exception as e:
        print(f"Error running climate agent: {e}")
    
    print()
    print("=" * 40)
    print()
    
    # Example 3: Climate Agent (Interactive Mode)
    print("3. Starting Climate Agent in Interactive Mode")
    print("   (This will start an interactive chat session)")
    print("   Type 'quit' to exit the climate agent")
    print()
    
    try:
        main(agent_type="climate")
    except KeyboardInterrupt:
        print("\nClimate agent session interrupted.")
    
    print()
    print("Example completed!")


if __name__ == "__main__":
    run_examples() 