"""Test script for the LangGraph climate agent."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_langgraph.climate_agent import ClimateAgent


class TestClimateAgent(unittest.TestCase):
    """Test cases for the ClimateAgent class."""

    def setUp(self):
        """Set up test environment."""
        # Set required environment variables
        os.environ["OPENAI_API_KEY"] = "test-api-key"
        os.environ["OPENAI_MODEL"] = "gpt-4.1-nano"
        os.environ["OPENAI_TEMPERATURE"] = "0"

    def tearDown(self):
        """Clean up test environment."""
        # Remove environment variables
        os.environ.pop("OPENAI_API_KEY", None)
        os.environ.pop("OPENAI_MODEL", None)
        os.environ.pop("OPENAI_TEMPERATURE", None)

    @patch('test_langgraph.climate_agent.ChatOpenAI')
    @patch('test_langgraph.climate_agent.ClimateDataService')
    def test_climate_agent_initialization(self, mock_climate_service, mock_chat_openai):
        """Test that ClimateAgent initializes correctly."""
        # Mock the ChatOpenAI instance
        mock_llm = MagicMock()
        mock_chat_openai.return_value = mock_llm
        
        # Mock the climate service
        mock_service = MagicMock()
        mock_climate_service.return_value = mock_service
        
        # Create the agent
        agent = ClimateAgent()
        
        # Verify initialization
        self.assertIsNotNone(agent)
        self.assertIsNotNone(agent.config)
        self.assertIsNotNone(agent.chatbot)
        self.assertIsNotNone(agent.logger)
        self.assertIsNotNone(agent.climate_service)
        self.assertIsNotNone(agent.llm)
        self.assertIsNotNone(agent.graph)
        
        # Verify ChatOpenAI was called with correct parameters
        mock_chat_openai.assert_called_once_with(
            api_key="test-api-key",
            temperature=0.0,
            model="gpt-4.1-nano"
        )

    def test_node_functions(self):
        """Test that node functions can be called."""
        agent = ClimateAgent()
        
        # Test climate researcher node
        state = {
            "city_name": "Test City",
            "research_data": None,
            "analysis_data": None,
            "advice_data": None,
            "messages": []
        }
        
        # Mock the LLM response
        mock_response = MagicMock()
        mock_response.content = "Test research data"
        agent.llm.invoke = MagicMock(return_value=mock_response)
        
        result = agent.climate_researcher(state)
        self.assertIsNotNone(result["research_data"])
        self.assertEqual(result["research_data"], "Test research data")


if __name__ == "__main__":
    unittest.main() 