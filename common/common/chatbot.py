"""Chatbot interface module for AI agent frameworks testing."""

import time
import logging
from datetime import datetime
from typing import Optional

from common.common.logging_config import get_logger


class ChatbotInterface:
    """A terminal-based chatbot interface with timestamp logging and configurable delays."""

    def __init__(self, response_delay: float = 1.0, log_level: str = "INFO"):
        """Initialize the chatbot interface.

        Args:
            response_delay: Delay in seconds between messages
            log_level: Logging level for the chatbot
        """
        self.response_delay = response_delay
        self.logger = get_logger("chatbot_interface")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        self.is_running = False

    def _get_timestamp(self) -> str:
        """Get current timestamp in formatted string.

        Returns:
            Formatted timestamp string
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def send_message(self, message: str) -> None:
        """Send a message and log it.

        Args:
            message: Message to send
        """
        self.logger.info(f"USER: {message}")
        time.sleep(self.response_delay)

    def receive_response(self, response: str) -> None:
        """Receive and log a response.

        Args:
            response: Response message to receive
        """
        self.logger.info(f"BOT: {response}")

    def start(self) -> None:
        """Start the interactive chatbot interface."""
        self.is_running = True
        self.logger.info("Chatbot interface started. Type 'quit' to exit.")

        while self.is_running:
            try:
                user_input = input(f"[{self._get_timestamp()}] You: ")
                
                if user_input.lower() in ["quit", "exit", "q"]:
                    self.logger.info("Chatbot interface stopped.")
                    self.is_running = False
                    break

                self.send_message(user_input)
                
                bot_response = self._generate_response(user_input)
                self.receive_response(bot_response)

            except KeyboardInterrupt:
                self.logger.warning("Chatbot interface interrupted.")
                self.is_running = False
                break
            except Exception as e:
                self.logger.error(f"Error: {str(e)}")

    def _generate_response(self, user_input: str) -> str:
        """Generate a response based on user input.

        Args:
            user_input: User's input message

        Returns:
            Generated response string
        """
        if "hello" in user_input.lower():
            return "Hello! How can I help you today?"
        elif "how are you" in user_input.lower():
            return "I'm doing well, thank you for asking!"
        elif "time" in user_input.lower():
            return f"The current time is {self._get_timestamp()}"
        elif "help" in user_input.lower():
            return "I'm a simple chatbot interface. You can ask me basic questions or type 'quit' to exit."
        else:
            return "I received your message. This is a test interface for AI agent frameworks."

    def stop(self) -> None:
        """Stop the chatbot interface."""
        self.is_running = False
        self.logger.info("Chatbot interface stopped.")

    def set_response_delay(self, delay: float) -> None:
        """Set the response delay between messages.

        Args:
            delay: Delay in seconds
        """
        self.response_delay = delay
        self.logger.debug(f"Response delay set to {delay} seconds.") 