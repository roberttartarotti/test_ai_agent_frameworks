# Common Library

A common library for AI agent frameworks testing that provides shared services and interfaces.

## Features

- Terminal-based chatbot interface with timestamp logging
- MongoDB climate data service for storing and retrieving city climate information
- Configurable time intervals and logging levels
- Importable by other AI agent framework test libraries

## Installation

```bash
pip install -e .
```

## Usage

### Chatbot Interface

```python
from common import ChatbotInterface

chatbot = ChatbotInterface()
chatbot.start()
```

### MongoDB Climate Service

```python
from common import ClimateDataService

service = ClimateDataService()
climate_data = service.get_city_climate("New York")
```

## Development

```bash
pip install -e .[dev]
``` 