"""Example usage of the chatbot interface."""

from common.chatbot import ChatbotInterface


def main():
    """Demonstrate the chatbot interface functionality.
    
    This function shows:
    1. How to create a chatbot interface
    2. How to send and receive messages
    3. How to start interactive mode
    """
    print("Starting Chatbot Interface Example")
    print("=" * 40)
    
    chatbot = ChatbotInterface(response_delay=0.5, log_level="INFO")
    
    print("Testing individual message methods:")
    chatbot.send_message("Hello, this is a test message")
    chatbot.receive_response("This is a test response")
    
    print("\n" + "=" * 40)
    print("Starting interactive mode (type 'quit' to exit):")
    chatbot.start()


if __name__ == "__main__":
    main() 