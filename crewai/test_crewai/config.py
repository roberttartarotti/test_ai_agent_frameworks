"""Configuration module for CrewAI test library."""

import os
from typing import Optional


class Config:
    """Configuration class for managing environment variables."""

    def __init__(self):
        """Initialize configuration with environment variables."""
        self.openai_api_key = self._get_openai_api_key()

    def _get_openai_api_key(self) -> str:
        """Get OpenAI API key from environment variable.

        Returns:
            OpenAI API key string.

        Raises:
            ValueError: If OPENAI_API_KEY environment variable is not set.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return api_key

    def get_llm_config(self) -> str:
        """Get LLM configuration string for CrewAI.

        Returns:
            LLM configuration string (model name).
        """
        return os.getenv("OPENAI_MODEL", "gpt-4.1-nano")

    def validate(self) -> bool:
        """Validate that all required configuration is present.

        Returns:
            True if configuration is valid.
        """
        return bool(self.openai_api_key) 