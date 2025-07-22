"""Configuration module for Agno test library."""

import os
from typing import Optional

from common.common.logging_config import get_logger

logger = get_logger("agno_config")


class Config:
    """Configuration class for managing environment variables."""

    def __init__(self):
        """Initialize configuration and load environment variables."""
        self.logger = get_logger("config")
        self.openai_api_key = self._get_openai_api_key()
        self.openai_model = self._get_openai_model()
        self.openai_temperature = self._get_openai_temperature()

    def _get_openai_api_key(self) -> str:
        """Get OpenAI API key from environment variables.

        Returns:
            OpenAI API key

        Raises:
            ValueError: If OPENAI_API_KEY is not set
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.logger.error("OPENAI_API_KEY environment variable is required")
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.logger.debug("OpenAI API key loaded successfully")
        return api_key

    def _get_openai_model(self) -> str:
        """Get OpenAI model from environment variables.

        Returns:
            OpenAI model name
        """
        model = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
        self.logger.debug(f"Using OpenAI model: {model}")
        return model

    def _get_openai_temperature(self) -> float:
        """Get OpenAI temperature from environment variables.

        Returns:
            Temperature value for OpenAI API
        """
        temperature = os.getenv("OPENAI_TEMPERATURE", "0.0")
        try:
            temp_value = float(temperature)
            self.logger.debug(f"Using temperature: {temp_value}")
            return temp_value
        except ValueError:
            self.logger.warning(f"Invalid temperature value: {temperature}, using default 0.0")
            return 0.0

    def validate(self) -> bool:
        """Validate configuration settings.

        Returns:
            True if configuration is valid, False otherwise
        """
        is_valid = bool(self.openai_api_key)
        if is_valid:
            self.logger.info("Configuration validation successful")
        else:
            self.logger.error("Configuration validation failed")
        return is_valid 