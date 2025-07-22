# AI Agent Frameworks Comparison

A comprehensive comparison of four popular AI agent frameworks: **CrewAI**, **LangChain**, **LangGraph**, and **Agno**. This project implements identical climate analysis functionality across all frameworks to provide a fair performance and feature comparison.

## 🏆 Performance Benchmark Results

Based on real-world testing with climate analysis queries for Paris, here are the performance results:

| Framework | Response Time | Status | Notes |
|-----------|---------------|--------|-------|
| **LangGraph** | **19.03s** | ✅ Success | Fastest framework with state-based workflow |
| **LangChain** | **20.25s** | ✅ Success | Good performance with sequential chains |
| **Agno** | **20.43s** | ✅ Success | Efficient single-agent approach |
| **CrewAI** | **45.28s** | ✅ Success | Multi-agent workflow with comprehensive output |

### Methodology
- **Test Query**: "What is the climate like in Paris?"
- **Environment**: Same OpenAI API key and model (gpt-4.1-nano)
- **Measurement**: End-to-end response time including API calls and database storage
- **Hardware**: Standard development environment (Linux 6.14.0-24-generic)
- **Date**: July 21, 2025
- **Test Runs**: Multiple iterations to ensure consistency

### Key Findings
- **LangGraph** demonstrated the best performance with its optimized state-based workflow
- **LangChain** and **Agno** showed similar performance with their respective approaches
- **CrewAI** took longer but provided the most comprehensive multi-agent analysis
- All frameworks successfully completed the climate analysis task with detailed, practical advice
- Response quality was consistently high across all frameworks

### Sample Responses

**LangGraph** (19.03s):
> "Absolutely! Here's a friendly, easy-to-understand guide to help you enjoy and prepare for life in Paris, considering its changing climate..."

**LangChain** (20.25s):
> "Hello! I'm here to help you understand Paris's climate in simple terms and give you practical tips to enjoy the city safely and comfortably all year round..."

**Agno** (20.43s):
> "Based on the detailed climate data for Paris, here are some friendly and practical insights to help you plan and stay comfortable throughout the year..."

**CrewAI** (45.28s):
> "If you're planning to visit or enjoy outdoor activities in Paris, understanding the climate throughout the year can help you make the most of your experience..."

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- MongoDB (optional, for data persistence)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd test_ai_agent_frameworks
   ```

2. **Set up environment**
   ```bash
   # Create virtual environment
   python -m venv env_ai_agents
   source env_ai_agents/bin/activate  # On Windows: env_ai_agents\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy and edit the environment file
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

4. **Install framework packages**
   ```bash
   # Install common library
   pip install -e ./common
   
   # Install framework packages
   pip install -e ./crewai
   pip install -e ./langchain
   pip install -e ./langgraph
   pip install -e ./agno
   ```

### Run the Comparison

```bash
# Run the benchmark comparison
python compare_agents.py
```

### Test Individual Frameworks

```bash
# CrewAI
start_crewai --city "Paris" --agent climate

# LangChain
start_langchain --city "Paris" --agent climate

# LangGraph
start_langgraph --city "Paris" --agent climate

# Agno
start_agno --city "Paris" --agent climate
```

## 📁 Project Structure

```
test_ai_agent_frameworks/
├── common/                 # Shared utilities and interfaces
│   ├── common/
│   │   ├── chatbot.py     # Terminal chatbot interface
│   │   ├── logging_config.py  # Centralized logging
│   │   └── mongodb/       # Database services
├── crewai/                # CrewAI implementation
│   └── test_crewai/
│       ├── climate_agent.py
│       ├── human_weather_agent.py
│       ├── config.py
│       └── main.py
├── langchain/             # LangChain implementation
│   └── test_langchain/
│       ├── climate_agent.py
│       ├── human_weather_agent.py
│       ├── config.py
│       └── main.py
├── langgraph/             # LangGraph implementation
│   └── test_langgraph/
│       ├── climate_agent.py
│       ├── human_weather_agent.py
│       ├── config.py
│       └── main.py
├── agno/                  # Agno implementation
│   └── test_agno/
│       ├── climate_agent.py
│       ├── human_weather_agent.py
│       ├── config.py
│       └── main.py
├── docs/                  # Sphinx documentation
├── compare_agents.py      # Benchmark script
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
└── README.md
```

## 🔧 Framework Implementations

### CrewAI
- **Pattern**: Multi-agent crew with sequential tasks
- **Strengths**: Comprehensive analysis, clear agent roles, built-in task management
- **Use Case**: Complex workflows requiring multiple specialized agents
- **Performance**: Slower but most detailed output

### LangChain
- **Pattern**: Sequential LLM chains
- **Strengths**: Simple to understand, extensive tool ecosystem, good performance
- **Use Case**: Straightforward sequential processing tasks
- **Performance**: Fast and reliable

### LangGraph
- **Pattern**: State-based workflow with nodes and edges
- **Strengths**: Flexible workflow control, state management, fastest performance
- **Use Case**: Complex workflows with conditional logic
- **Performance**: Fastest framework tested

### Agno
- **Pattern**: Single agent with multiple specialized prompts
- **Strengths**: Clean API, efficient resource usage, good performance
- **Use Case**: Single-agent applications with multiple capabilities
- **Performance**: Fast and efficient

## 📊 Features Comparison

| Feature | CrewAI | LangChain | LangGraph | Agno |
|---------|--------|-----------|-----------|------|
| Multi-agent Support | ✅ | ❌ | ✅ | ❌ |
| State Management | ✅ | ❌ | ✅ | ❌ |
| Task Sequencing | ✅ | ✅ | ✅ | ❌ |
| Memory Management | ✅ | ✅ | ✅ | ✅ |
| Tool Integration | ✅ | ✅ | ✅ | ✅ |
| Error Handling | ✅ | ✅ | ✅ | ✅ |
| Logging | ✅ | ✅ | ✅ | ✅ |
| MongoDB Integration | ✅ | ✅ | ✅ | ✅ |
| Response Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Performance | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🧪 Testing

```bash
# Run all tests
pytest

# Run framework-specific tests
pytest crewai/
pytest langchain/
pytest langgraph/
pytest agno/

# Run benchmark comparison
python compare_agents.py
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

```bash
# Build documentation
cd docs
make html
make latexpdf
```

## 🔍 Recent Updates

- ✅ Fixed all import issues across frameworks
- ✅ Implemented centralized logging system
- ✅ Added comprehensive error handling
- ✅ Created automated benchmark script
- ✅ Fixed CrewAI result extraction
- ✅ Updated all framework implementations
- ✅ Added MongoDB integration
- ✅ Created detailed documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT models
- The CrewAI, LangChain, LangGraph, and Agno development teams
- MongoDB for the database solution

---

**Note**: Performance results may vary based on network conditions, API response times, and system resources. This comparison is based on multiple test runs and should be considered as a reference point rather than definitive performance metrics. All frameworks provide high-quality responses suitable for production use.
