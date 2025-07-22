# CrewAI Climate Agent

A CrewAI-based agent for providing comprehensive climate information about cities using MongoDB for data storage and the common chatbot interface.

## Features

- **Multi-Agent System**: Three specialized agents working together:
  - Climate Researcher: Gathers comprehensive climate data
  - Climate Analyst: Analyzes patterns and trends
  - Climate Advisor: Provides user-friendly advice
- **MongoDB Integration**: Local database for storing and retrieving climate information
- **Common Interface**: Uses the shared chatbot interface from the common library
- **Environment Configuration**: Secure handling of OpenAI API credentials
- **Interactive Mode**: Terminal-based interactive climate assistant

## Installation

```bash
pip install -e .
```

## Environment Setup

Set the following environment variables:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_MODEL="gpt-3.5-turbo"  # Optional, defaults to gpt-3.5-turbo
```

## Usage

### Command Line Interface

Start the interactive climate agent:

```bash
start_crewai
```

Analyze climate for a specific city:

```bash
start_crewai --city "New York"
```

### Programmatic Usage

```python
from test_crewai import ClimateAgent

# Initialize the agent
agent = ClimateAgent()

# Get climate information for a city
climate_info = agent.get_climate_info("Tokyo")

# Start interactive mode
agent.start_interactive_mode()

# Clean up
agent.close()
```

## Architecture

### Agents

1. **Climate Researcher Agent**
   - Role: Research and data gathering
   - Goal: Provide accurate climate information
   - Responsibilities: Temperature, precipitation, humidity, seasonal patterns

2. **Climate Analyst Agent**
   - Role: Data analysis and insights
   - Goal: Identify patterns and trends
   - Responsibilities: Pattern recognition, trend analysis, recommendations

3. **Climate Advisor Agent**
   - Role: User-friendly advice
   - Goal: Provide practical recommendations
   - Responsibilities: Activity suggestions, travel advice, seasonal tips

### Data Flow

1. User requests climate information for a city
2. Climate Researcher gathers comprehensive data
3. Climate Analyst processes and analyzes the data
4. Climate Advisor provides user-friendly recommendations
5. Results are stored in MongoDB for future reference

## MongoDB Schema

Climate data is stored in the `climate_db.city_climate` collection:

```json
{
    "city": "City Name",
    "research": "Detailed climate research findings",
    "analysis": "Climate analysis and insights",
    "advice": "Practical recommendations and advice",
    "timestamp": "2024-01-01T00:00:00Z"
}
```

## Configuration

The agent uses environment variables for configuration:

- `OPENAI_API_KEY`: Required OpenAI API key
- `OPENAI_MODEL`: Optional model name (default: gpt-3.5-turbo)

## Dependencies

- `crewai`: Multi-agent framework with built-in LLM support
- `pymongo`: MongoDB client
- `common`: Shared chatbot interface

## Development

```bash
pip install -e .[dev]
```

## Testing

```bash
python test_climate_agent.py
```

## Examples

### Interactive Session

```
[2024-01-01 12:00:00] You: What's the climate like in Paris?
[2024-01-01 12:00:00] BOT: Researching climate information for Paris...
[2024-01-01 12:00:01] BOT: Here's what I found about Paris's climate:

Paris has a temperate oceanic climate with mild winters and warm summers. 
Average temperatures range from 3°C in winter to 25°C in summer. 
Precipitation is evenly distributed throughout the year with about 650mm annually.

Best times to visit: Spring (March-May) and Fall (September-November)
What to pack: Light layers for spring/fall, warm clothes for winter
Activities: Outdoor cafes in summer, museums in winter
```

### Programmatic Analysis

```python
climate_info = agent.get_climate_info("London")
print(f"Research: {climate_info['research']}")
print(f"Analysis: {climate_info['analysis']}")
print(f"Advice: {climate_info['advice']}")
``` 