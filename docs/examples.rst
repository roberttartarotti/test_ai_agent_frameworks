Examples
========

This section provides practical examples of how to use each AI agent framework for climate and weather analysis.

Quick Start Examples
-------------------

Basic Climate Analysis
~~~~~~~~~~~~~~~~~~~~~

**CrewAI Example:**
.. code-block:: python
   
   from test_crewai import ClimateAgent
   
   agent = ClimateAgent()
   climate_info = agent.get_climate_info("Paris")
   print(f"Climate Analysis: {climate_info['advice']}")

**LangChain Example:**
.. code-block:: python
   
   from test_langchain import ClimateAgent
   
   agent = ClimateAgent()
   climate_info = agent.get_climate_info("Tokyo")
   print(f"Climate Analysis: {climate_info['advice']}")

**LangGraph Example:**
.. code-block:: python
   
   from test_langgraph import ClimateAgent
   
   agent = ClimateAgent()
   climate_info = agent.get_climate_info("London")
   print(f"Climate Analysis: {climate_info['advice']}")

**Agno Example:**
.. code-block:: python
   
   from test_agno import ClimateAgent
   
   agent = ClimateAgent()
   climate_info = agent.get_climate_info("New York")
   print(f"Climate Analysis: {climate_info['advice']}")

Weather Query Examples
~~~~~~~~~~~~~~~~~~~~~

**CrewAI Weather Agent:**
.. code-block:: python
   
   from test_crewai import HumanWeatherAgent
   
   agent = HumanWeatherAgent()
   response = agent.process_weather_query("What's the temperature in Tokyo?")
   print(f"Weather Response: {response}")

**LangChain Weather Agent:**
.. code-block:: python
   
   from test_langchain import HumanWeatherAgent
   
   agent = HumanWeatherAgent()
   response = agent.process_weather_query("Compare temperatures between Paris and London")
   print(f"Weather Response: {response}")

**LangGraph Weather Agent:**
.. code-block:: python
   
   from test_langgraph import HumanWeatherAgent
   
   agent = HumanWeatherAgent()
   response = agent.process_weather_query("Get weather summary for all cities")
   print(f"Weather Response: {response}")

**Agno Weather Agent:**
.. code-block:: python
   
   from test_agno import HumanWeatherAgent
   
   agent = HumanWeatherAgent()
   response = agent.process_weather_query("What's the current temperature in Berlin?")
   print(f"Weather Response: {response}")

Interactive Mode Examples
------------------------

**Starting Interactive Mode:**
.. code-block:: python
   
   # CrewAI
   from test_crewai.main import main
   main(agent_type="weather")  # or "climate"
   
   # LangChain
   from test_langchain.main import main
   main(agent_type="weather")  # or "climate"
   
   # LangGraph
   from test_langgraph.main import main
   main(agent_type="weather")  # or "climate"
   
   # Agno
   from test_agno.main import main
   main(agent_type="weather")  # or "climate"

**Command Line Usage:**
.. code-block:: bash
   
   # CrewAI
   cd crewai && start_crewai --agent weather
   cd crewai && start_crewai --agent climate --city "Paris"
   
   # LangChain
   cd langchain && start_langchain --agent weather
   cd langchain && start_langchain --agent climate --city "Tokyo"
   
   # LangGraph
   cd langgraph && start_langgraph --agent weather
   cd langgraph && start_langgraph --agent climate --city "London"
   
   # Agno
   cd agno && start_agno --agent weather
   cd agno && start_agno --agent climate --city "New York"

Advanced Examples
----------------

Custom Configuration
~~~~~~~~~~~~~~~~~~~

**Environment Setup:**
.. code-block:: python
   
   import os
   from test_agno import ClimateAgent
   
   # Custom configuration
   os.environ["OPENAI_MODEL"] = "gpt-4"
   os.environ["OPENAI_TEMPERATURE"] = "0.7"
   
   agent = ClimateAgent()
   climate_info = agent.get_climate_info("Sydney")

**Custom Logging:**
.. code-block:: python
   
   from common import get_logger
   from test_langchain import ClimateAgent
   
   logger = get_logger("custom_app")
   logger.setLevel("DEBUG")
   
   agent = ClimateAgent()
   logger.info("Starting climate analysis")
   climate_info = agent.get_climate_info("Moscow")

Data Integration Examples
~~~~~~~~~~~~~~~~~~~~~~~~

**MongoDB Integration:**
.. code-block:: python
   
   from common import ClimateDataService
   from test_crewai import ClimateAgent
   
   # Initialize services
   climate_service = ClimateDataService()
   agent = ClimateAgent()
   
   # Get climate info and store in database
   climate_info = agent.get_climate_info("Rome")
   climate_service.insert_city_climate(climate_info)
   
   # Retrieve stored data
   stored_data = climate_service.get_city_climate("Rome")
   print(f"Stored data: {stored_data}")

**Temperature Tools Usage:**
.. code-block:: python
   
   from common import TemperatureTools
   
   tools = TemperatureTools()
   
   # Get current temperature
   temp_data = tools.get_current_temperature("Paris")
   print(f"Current temperature: {temp_data}")
   
   # Compare cities
   comparison = tools.get_temperature_comparison("Paris", "London")
   print(f"Comparison: {comparison}")
   
   # Get weather summary
   summary = tools.get_weather_summary()
   print(f"Summary: {summary}")

Error Handling Examples
~~~~~~~~~~~~~~~~~~~~~~

**Robust Error Handling:**
.. code-block:: python
   
   from test_langgraph import ClimateAgent
   from common import get_logger
   
   logger = get_logger("error_handling")
   
   try:
       agent = ClimateAgent()
       climate_info = agent.get_climate_info("InvalidCity")
   except Exception as e:
       logger.error(f"Error analyzing climate: {e}")
       climate_info = {"error": "Unable to analyze climate data"}

**Configuration Validation:**
.. code-block:: python
   
   from test_agno.config import Config
   
   try:
       config = Config()
       if config.validate():
           print("Configuration is valid")
       else:
           print("Configuration validation failed")
   except ValueError as e:
       print(f"Configuration error: {e}")

Testing Examples
---------------

**Unit Testing:**
.. code-block:: python
   
   import unittest
   from unittest.mock import patch, MagicMock
   from test_agno import ClimateAgent
   
   class TestClimateAgent(unittest.TestCase):
       def setUp(self):
           self.agent = ClimateAgent()
       
       @patch('test_agno.climate_agent.Agent')
       def test_climate_analysis(self, mock_agent):
           mock_agent.return_value.run.return_value = "Test climate data"
           result = self.agent.get_climate_info("TestCity")
           self.assertIn("advice", result)
   
   if __name__ == "__main__":
       unittest.main()

**Integration Testing:**
.. code-block:: python
   
   import pytest
   from test_langchain import ClimateAgent
   from common import ClimateDataService
   
   @pytest.fixture
   def climate_agent():
       return ClimateAgent()
   
   @pytest.fixture
   def climate_service():
       return ClimateDataService()
   
   def test_end_to_end_workflow(climate_agent, climate_service):
       # Test complete workflow
       climate_info = climate_agent.get_climate_info("Berlin")
       assert "city" in climate_info
       assert "advice" in climate_info
       
       # Test database integration
       climate_service.insert_city_climate(climate_info)
       stored_data = climate_service.get_city_climate("Berlin")
       assert stored_data is not None

Performance Testing Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Benchmarking:**
.. code-block:: python
   
   import time
   from test_crewai import ClimateAgent
   
   def benchmark_climate_analysis():
       agent = ClimateAgent()
       cities = ["Paris", "Tokyo", "London", "New York", "Sydney"]
       
       results = {}
       for city in cities:
           start_time = time.time()
           climate_info = agent.get_climate_info(city)
           end_time = time.time()
           
           results[city] = {
               "time": end_time - start_time,
               "success": "advice" in climate_info
           }
       
       return results
   
   # Run benchmark
   benchmark_results = benchmark_climate_analysis()
   for city, result in benchmark_results.items():
       print(f"{city}: {result['time']:.2f}s ({result['success']})")

**Memory Profiling:**
.. code-block:: python
   
   import psutil
   import os
   from test_langchain import ClimateAgent
   
   def profile_memory_usage():
       process = psutil.Process(os.getpid())
       initial_memory = process.memory_info().rss / 1024 / 1024  # MB
       
       agent = ClimateAgent()
       agent_memory = process.memory_info().rss / 1024 / 1024  # MB
       
       climate_info = agent.get_climate_info("Paris")
       final_memory = process.memory_info().rss / 1024 / 1024  # MB
       
       return {
           "initial": initial_memory,
           "after_agent": agent_memory,
           "after_analysis": final_memory,
           "agent_overhead": agent_memory - initial_memory,
           "analysis_overhead": final_memory - agent_memory
       }
   
   # Run memory profile
   memory_profile = profile_memory_usage()
   print(f"Memory Profile: {memory_profile}")

Complete Application Example
---------------------------

**Full Application with Error Handling:**
.. code-block:: python
   
   import os
   import sys
   from typing import Optional
   from common import get_logger
   from test_agno import ClimateAgent, HumanWeatherAgent
   
   logger = get_logger("complete_app")
   
   class ClimateWeatherApp:
       def __init__(self):
           self.climate_agent = None
           self.weather_agent = None
           self.setup_agents()
       
       def setup_agents(self):
           """Initialize agents with error handling."""
           try:
               self.climate_agent = ClimateAgent()
               self.weather_agent = HumanWeatherAgent()
               logger.info("Agents initialized successfully")
           except Exception as e:
               logger.error(f"Failed to initialize agents: {e}")
               sys.exit(1)
       
       def analyze_climate(self, city: str) -> Optional[dict]:
           """Analyze climate for a city."""
           try:
               logger.info(f"Analyzing climate for {city}")
               return self.climate_agent.get_climate_info(city)
           except Exception as e:
               logger.error(f"Climate analysis failed for {city}: {e}")
               return None
       
       def get_weather_info(self, query: str) -> Optional[str]:
           """Get weather information."""
           try:
               logger.info(f"Processing weather query: {query}")
               return self.weather_agent.process_weather_query(query)
           except Exception as e:
               logger.error(f"Weather query failed: {e}")
               return None
       
       def run_interactive_mode(self, agent_type: str = "weather"):
           """Run interactive mode."""
           try:
               if agent_type == "weather":
                   self.weather_agent.start_interactive_mode()
               else:
                   self.climate_agent.start_interactive_mode()
           except KeyboardInterrupt:
               logger.info("Interactive mode interrupted by user")
           except Exception as e:
               logger.error(f"Interactive mode failed: {e}")
       
       def cleanup(self):
           """Clean up resources."""
           try:
               if self.climate_agent:
                   self.climate_agent.close()
               if self.weather_agent:
                   self.weather_agent.close()
               logger.info("Cleanup completed")
           except Exception as e:
               logger.error(f"Cleanup failed: {e}")
   
   def main():
       """Main application entry point."""
       app = ClimateWeatherApp()
       
       try:
           # Example usage
           climate_info = app.analyze_climate("Paris")
           if climate_info:
               print(f"Climate Analysis: {climate_info['advice']}")
           
           weather_info = app.get_weather_info("What's the temperature in Tokyo?")
           if weather_info:
               print(f"Weather Info: {weather_info}")
           
           # Run interactive mode
           app.run_interactive_mode("weather")
           
       finally:
           app.cleanup()
   
   if __name__ == "__main__":
       main()

These examples demonstrate the practical usage of each framework and provide a foundation for building more complex applications. 