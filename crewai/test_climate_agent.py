"""Test script for the climate agent."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_crewai.climate_agent import ClimateAgent


class TestClimateAgent(unittest.TestCase):
    """Test cases for the ClimateAgent class."""

    def setUp(self):
        """Set up test environment."""
        # Set required environment variables
        os.environ["OPENAI_API_KEY"] = "test-api-key"
        os.environ["OPENAI_MODEL"] = "gpt-3.5-turbo"

    def tearDown(self):
        """Clean up test environment."""
        # Remove environment variables
        os.environ.pop("OPENAI_API_KEY", None)
        os.environ.pop("OPENAI_MODEL", None)

    @patch('test_crewai.climate_agent.ClimateDataService')
    def test_climate_agent_initialization(self, mock_climate_service):
        """Test that ClimateAgent initializes correctly."""
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
        
        # Verify LLM config
        self.assertEqual(agent.config.get_llm_config(), "gpt-3.5-turbo")

    def test_agent_creation(self):
        """Test that agents can be created with string LLM config."""
        agent = ClimateAgent()
        
        # Test creating agents
        researcher = agent.create_climate_researcher_agent()
        analyst = agent.create_climate_analyst_agent()
        advisor = agent.create_climate_advisor_agent()
        
        self.assertIsNotNone(researcher)
        self.assertIsNotNone(analyst)
        self.assertIsNotNone(advisor)


if __name__ == "__main__":
    unittest.main() 