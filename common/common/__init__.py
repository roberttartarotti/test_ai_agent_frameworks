"""Common library for AI agent frameworks testing."""

from .chatbot import ChatbotInterface
from .mongodb.climate_data import ClimateDataService
from .mongodb.tools import TemperatureTools
from .logging_config import LoggingConfig, setup_logging, get_logger

__version__ = "0.1.0"
__all__ = [
    "ChatbotInterface", 
    "ClimateDataService", 
    "TemperatureTools",
    "LoggingConfig",
    "setup_logging",
    "get_logger"
] 