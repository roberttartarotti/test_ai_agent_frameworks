Installation Guide
=================

This guide will help you set up the AI Agent Frameworks Testing project on your system.

Prerequisites
------------

* **Python 3.8+**: All frameworks require Python 3.8 or higher
* **MongoDB**: For data persistence (optional, can use mock data)
* **OpenAI API Key**: Required for all AI agent functionality
* **Git**: For cloning the repository

System Requirements
------------------

* **Operating System**: Linux, macOS, or Windows
* **Memory**: Minimum 4GB RAM (8GB recommended)
* **Storage**: 2GB free space
* **Network**: Internet connection for API calls

Installation Steps
-----------------

1. **Clone the Repository**
   .. code-block:: bash
      
      git clone <repository-url>
      cd test_ai_agent_frameworks

2. **Create Virtual Environment**
   .. code-block:: bash
      
      python -m venv .venv
      source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install Common Library**
   .. code-block:: bash
      
      cd common
      pip install -e .

4. **Install Framework Libraries**
   .. code-block:: bash
      
      # CrewAI
      cd ../crewai
      pip install -e .
      
      # LangChain
      cd ../langchain
      pip install -e .
      
      # LangGraph
      cd ../langgraph
      pip install -e .
      
      # Agno
      cd ../agno
      pip install -e .

5. **Install Development Dependencies**
   .. code-block:: bash
      
      pip install pytest pytest-cov black ruff mypy pre-commit

Environment Configuration
------------------------

1. **Set OpenAI API Key**
   .. code-block:: bash
      
      export OPENAI_API_KEY="your-openai-api-key-here"

2. **Configure Model Settings**
   .. code-block:: bash
      
      export OPENAI_MODEL="gpt-4.1-nano"
      export OPENAI_TEMPERATURE="0.0"

3. **Optional: MongoDB Setup**
   .. code-block:: bash
      
      # Install MongoDB (Ubuntu/Debian)
      sudo apt update
      sudo apt install mongodb
      
      # Start MongoDB service
      sudo systemctl start mongodb
      sudo systemctl enable mongodb

Verification
-----------

1. **Test Common Library**
   .. code-block:: bash
      
      cd common
      python example.py

2. **Test Framework Installations**
   .. code-block:: bash
      
      # Test CrewAI
      cd ../crewai
      python -c "from test_crewai import ClimateAgent; print('CrewAI OK')"
      
      # Test LangChain
      cd ../langchain
      python -c "from test_langchain import ClimateAgent; print('LangChain OK')"
      
      # Test LangGraph
      cd ../langgraph
      python -c "from test_langgraph import ClimateAgent; print('LangGraph OK')"
      
      # Test Agno
      cd ../agno
      python -c "from test_agno import ClimateAgent; print('Agno OK')"

3. **Run Unit Tests**
   .. code-block:: bash
      
      pytest common/test_chatbot.py -v
      pytest agno/test_climate_agent.py -v

Configuration Files
------------------

The project uses several configuration files:

**pyproject.toml**
   Project metadata and dependencies for each framework

**setup.py**
   Alternative dependency definition for setuptools

**conf.py** (Sphinx)
   Documentation configuration

**pre-commit-config.yaml**
   Code quality hooks

Troubleshooting
--------------

**Common Issues:**

1. **Import Errors**
   * Ensure virtual environment is activated
   * Check that all packages are installed with `-e` flag
   * Verify Python path includes project root

2. **API Key Errors**
   * Verify OPENAI_API_KEY is set correctly
   * Check API key permissions and quota
   * Ensure internet connectivity

3. **MongoDB Connection Issues**
   * Verify MongoDB service is running
   * Check connection string in ClimateDataService
   * Ensure MongoDB port (27017) is accessible

4. **Framework-Specific Issues**
   * CrewAI: Check crewai version compatibility
   * LangChain: Verify langchain version
   * LangGraph: Ensure langgraph dependencies
   * Agno: Check agno package installation

**Debug Mode:**
   .. code-block:: bash
      
      export LOG_LEVEL="DEBUG"
      python -m pytest -v --tb=short

Performance Optimization
-----------------------

1. **Memory Usage**
   * Use smaller models for testing
   * Implement proper cleanup in agents
   * Monitor memory usage with profiling tools

2. **Response Time**
   * Optimize agent configurations
   * Use caching for repeated queries
   * Implement async processing where possible

3. **Database Performance**
   * Index MongoDB collections
   * Use connection pooling
   * Implement query optimization

Development Setup
----------------

1. **Install Development Tools**
   .. code-block:: bash
      
      pip install black ruff mypy pre-commit
      pre-commit install

2. **Configure IDE**
   * Set Python interpreter to virtual environment
   * Enable type checking
   * Configure linting and formatting

3. **Set Up Testing**
   .. code-block:: bash
      
      pytest --cov=common --cov=test_crewai --cov=test_langchain --cov=test_langgraph --cov=test_agno

4. **Documentation Development**
   .. code-block:: bash
      
      cd docs
      make html
      make latexpdf

This setup provides a complete development environment for working with all four AI agent frameworks. 