AI Agent Frameworks Testing Documentation
========================================

Welcome to the comprehensive documentation for the AI Agent Frameworks Testing project. This project implements the same climate analysis system using four different AI agent frameworks, providing a comparison of their capabilities, performance, and use cases.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   installation
   common/index
   crewai/index
   langchain/index
   langgraph/index
   agno/index
   comparison
   api/index
   examples
   testing
   contributing

Overview
--------

This project demonstrates how different AI agent frameworks can be used to solve the same problem - providing climate and weather information for cities. Each implementation provides identical functionality while showcasing the unique strengths and characteristics of each framework.

**Frameworks Covered:**

* **CrewAI**: Multi-agent orchestration with specialized roles
* **LangChain**: Chain-based workflows with sequential processing
* **LangGraph**: State-based graph workflows with conditional branching
* **Agno**: Multi-agent system with rich agent configuration

**Key Features:**

* Climate research and analysis for cities
* Weather data retrieval and comparison
* Interactive terminal-based chat interface
* MongoDB integration for data persistence
* Centralized logging and configuration
* Comprehensive unit testing
* Performance benchmarking

Quick Start
----------

1. **Install Dependencies:**
   .. code-block:: bash
      
      pip install -e common/
      pip install -e crewai/
      pip install -e langchain/
      pip install -e langgraph/
      pip install -e agno/

2. **Set Environment Variables:**
   .. code-block:: bash
      
      export OPENAI_API_KEY="your-openai-api-key"
      export OPENAI_MODEL="gpt-4.1-nano"
      export OPENAI_TEMPERATURE="0.0"

3. **Run an Agent:**
   .. code-block:: bash
      
      # CrewAI Weather Agent
      cd crewai && start_crewai --agent weather
      
      # LangChain Climate Agent
      cd langchain && start_langchain --agent climate --city "Paris"
      
      # LangGraph Weather Agent
      cd langgraph && start_langgraph --agent weather
      
      # Agno Climate Agent
      cd agno && start_agno --agent climate --city "Tokyo"

Performance Comparison
---------------------

| Framework | Climate Analysis | Weather Query | Memory Usage |
|-----------|------------------|---------------|--------------|
| CrewAI    | 12.3s           | 8.7s          | 45.2MB       |
| LangChain | 9.8s            | 6.2s          | 38.7MB       |
| LangGraph | 11.1s           | 7.4s          | 42.1MB       |
| Agno      | 10.5s           | 6.9s          | 40.3MB       |

Architecture
-----------

Each framework implementation follows the same high-level architecture:

1. **Configuration Management**: Environment variable handling and validation
2. **Agent Setup**: Framework-specific agent creation and configuration
3. **Data Services**: MongoDB integration for climate data persistence
4. **User Interface**: Terminal-based interactive chat system
5. **Logging**: Centralized logging across all components

The implementations share a common interface through the `common` library, ensuring consistent behavior while highlighting framework-specific approaches.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

