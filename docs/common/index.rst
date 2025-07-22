Common Library
==============

The common library provides shared functionality across all AI agent framework implementations. This ensures consistent behavior while allowing each framework to showcase its unique capabilities.

.. toctree::
   :maxdepth: 2
   :caption: Common Library:

   modules/chatbot
   modules/logging_config
   modules/mongodb

Overview
--------

The common library consists of several key components:

* **ChatbotInterface**: Terminal-based user interaction system
* **ClimateDataService**: MongoDB data persistence layer
* **TemperatureTools**: Weather data management utilities
* **LoggingConfig**: Centralized logging configuration

These components provide a consistent foundation for all framework implementations, ensuring that differences in behavior are due to framework characteristics rather than implementation details.

Architecture
-----------

.. image:: ../_static/common_architecture.png
   :alt: Common Library Architecture
   :align: center

**Key Features:**

* **Modular Design**: Each component is self-contained and reusable
* **Type Safety**: Full type hints throughout the codebase
* **Error Handling**: Comprehensive error handling and logging
* **Configuration**: Environment-based configuration management
* **Testing**: Unit tests for all components

Usage Examples
-------------

**Basic Chatbot Interface:**
.. code-block:: python
   
   from common import ChatbotInterface
   
   chatbot = ChatbotInterface(response_delay=0.5, log_level="INFO")
   chatbot.send_message("Hello, user!")
   chatbot.receive_response("Hello, bot!")

**Climate Data Service:**
.. code-block:: python
   
   from common import ClimateDataService
   
   service = ClimateDataService()
   service.insert_city_climate({
       "city": "Paris",
       "temperature": 20.5,
       "humidity": 65.0
   })

**Temperature Tools:**
.. code-block:: python
   
   from common import TemperatureTools
   
   tools = TemperatureTools()
   temp_data = tools.get_current_temperature("Tokyo")
   print(f"Current temperature: {temp_data}")

**Logging Configuration:**
.. code-block:: python
   
   from common import get_logger
   
   logger = get_logger("my_module")
   logger.info("Application started")

API Reference
-------------

.. automodule:: common
   :members:
   :undoc-members:
   :show-inheritance:

Components
----------

Chatbot Interface
~~~~~~~~~~~~~~~~~

The ChatbotInterface provides a terminal-based interaction system with configurable delays and logging.

.. automodule:: common.chatbot
   :members:
   :undoc-members:
   :show-inheritance:

Climate Data Service
~~~~~~~~~~~~~~~~~~~

The ClimateDataService manages MongoDB operations for climate data persistence.

.. automodule:: common.mongodb.climate_data
   :members:
   :undoc-members:
   :show-inheritance:

Temperature Tools
~~~~~~~~~~~~~~~~

The TemperatureTools provide utilities for managing and querying temperature data.

.. automodule:: common.mongodb.tools
   :members:
   :undoc-members:
   :show-inheritance:

Logging Configuration
~~~~~~~~~~~~~~~~~~~~

The LoggingConfig provides centralized logging setup and management.

.. automodule:: common.logging_config
   :members:
   :undoc-members:
   :show-inheritance:

Data Models
----------

Temperature Data Model
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: common.mongodb.tools
   :members: TemperatureData
   :undoc-members:
   :show-inheritance:

Configuration
------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~

* **OPENAI_API_KEY**: Required for AI agent functionality
* **OPENAI_MODEL**: Model to use (default: gpt-4.1-nano)
* **OPENAI_TEMPERATURE**: Model temperature (default: 0.0)
* **MONGODB_URI**: MongoDB connection string (default: mongodb://localhost:27017/)

MongoDB Schema
~~~~~~~~~~~~~

The climate data is stored in the following schema:

.. code-block:: json
   
   {
     "city": "string",
     "temperature_celsius": "float",
     "humidity_percent": "float",
     "weather_condition": "string",
     "timestamp": "datetime",
     "climate_type": "string",
     "seasonal_info": "object"
   }

Testing
-------

The common library includes comprehensive unit tests:

.. code-block:: bash
   
   pytest common/test_chatbot.py -v
   pytest common/test_mongodb.py -v

Performance Considerations
-------------------------

* **Connection Pooling**: MongoDB connections are pooled for efficiency
* **Lazy Loading**: Components are initialized only when needed
* **Memory Management**: Proper cleanup of resources
* **Async Support**: Future-ready for async operations

Best Practices
-------------

1. **Error Handling**: Always handle exceptions from external services
2. **Logging**: Use appropriate log levels for different types of messages
3. **Configuration**: Use environment variables for configuration
4. **Testing**: Write unit tests for all components
5. **Documentation**: Maintain comprehensive docstrings

This common library provides a solid foundation for all AI agent framework implementations while maintaining clean separation of concerns and promoting code reuse. 