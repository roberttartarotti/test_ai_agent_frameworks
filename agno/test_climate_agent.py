"""Test script for the Agno climate agent."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_agno.climate_agent import ClimateAgent


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

    @patch('test_agno.climate_agent.Agent')
    @patch('test_agno.climate_agent.ClimateDataService')
    def test_climate_agent_initialization(self, mock_climate_service, mock_agent):
        """Test that ClimateAgent initializes correctly."""
        # Mock the Agent instances
        mock_researcher = MagicMock()
        mock_analyst = MagicMock()
        mock_advisor = MagicMock()
        mock_agent.side_effect = [mock_researcher, mock_analyst, mock_advisor]
        
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
        self.assertIsNotNone(agent.openai_client)
        self.assertIsNotNone(agent.agents)
        
        # Verify agents were created
        self.assertIn("researcher", agent.agents)
        self.assertIn("analyst", agent.agents)
        self.assertIn("advisor", agent.agents)

    def test_agent_configuration(self):
        """Test that agent configurations are correct."""
        agent = ClimateAgent()
        
        # Test that agents have the expected structure
        for agent_name, agno_agent in agent.agents.items():
            self.assertIsNotNone(agno_agent)
            # Verify the agent has a run method (basic Agno agent functionality)
            self.assertTrue(hasattr(agno_agent, 'run'))


if __name__ == "__main__":
    unittest.main() 