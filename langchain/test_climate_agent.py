"""Test script for the LangChain climate agent."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_langchain.climate_agent import ClimateAgent


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

    @patch('test_langchain.climate_agent.ChatOpenAI')
    @patch('test_langchain.climate_agent.ClimateDataService')
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
        
        # Verify ChatOpenAI was called with correct parameters
        mock_chat_openai.assert_called_once_with(
            api_key="test-api-key",
            temperature=0.0,
            model="gpt-4.1-nano"
        )

    def test_prompt_creation(self):
        """Test that prompt templates can be created."""
        agent = ClimateAgent()
        
        # Test creating prompts
        research_prompt = agent.create_climate_researcher_prompt()
        analysis_prompt = agent.create_climate_analyst_prompt()
        advice_prompt = agent.create_climate_advisor_prompt()
        
        self.assertIsNotNone(research_prompt)
        self.assertIsNotNone(analysis_prompt)
        self.assertIsNotNone(advice_prompt)


if __name__ == "__main__":
    unittest.main() 