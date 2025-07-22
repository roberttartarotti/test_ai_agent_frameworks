"""Configuration module for LangGraph test library."""

import os
from typing import Optional


class Config:
    """Configuration class for managing environment variables."""

    def __init__(self):
        """Initialize configuration with environment variables."""
        self.openai_api_key = self._get_openai_api_key()
        self.openai_model = self._get_openai_model()
        self.openai_temperature = self._get_openai_temperature()

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

    def _get_openai_model(self) -> str:
        """Get OpenAI model from environment variable.

        Returns:
            OpenAI model string, defaults to "gpt-4.1-nano" if not set.
        """
        return os.getenv("OPENAI_MODEL", "gpt-4.1-nano")

    def _get_openai_temperature(self) -> float:
        """Get OpenAI temperature from environment variable.

        Returns:
            OpenAI temperature as float, defaults to 0.0 if not set.
        """
        temperature = os.getenv("OPENAI_TEMPERATURE", "0.0")
        try:
            return float(temperature)
        except ValueError:
            return 0.0

    def validate(self) -> bool:
        """Validate that all required configuration is present.

        Returns:
            True if configuration is valid.
        """
        return bool(self.openai_api_key) 