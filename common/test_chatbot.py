"""Test script for the chatbot interface."""

from common.chatbot import ChatbotInterface


def test_chatbot_basic():
    """Test basic chatbot functionality."""
    chatbot = ChatbotInterface(response_delay=0.1, log_level="DEBUG")
    
    chatbot.send_message("Hello")
    chatbot.receive_response("Hi there!")
    
    chatbot.send_message("What time is it?")
    chatbot.receive_response("The time is now")


if __name__ == "__main__":
    test_chatbot_basic()
    print("Basic test completed successfully!") 