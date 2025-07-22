# MongoDB Climate Data Service

A local MongoDB service for storing and retrieving climate data for cities.

## Features

- Store climate information for cities
- Retrieve climate data by city name
- Update existing climate records
- Get database statistics
- Automatic timestamp tracking

## Usage

```python
from climate_data import ClimateDataService

# Initialize the service
service = ClimateDataService()

# Insert climate data
city_data = {
    "city": "New York",
    "temperature": {"min": 10, "max": 25, "avg": 17.5},
    "precipitation": {"annual": 1200, "unit": "mm"},
    "humidity": {"avg": 65, "unit": "%"},
    "climate_type": "Humid subtropical"
}

service.insert_city_climate(city_data)

# Retrieve climate data
climate_info = service.get_city_climate("New York")

# Get all cities
cities = service.get_all_cities()

# Close connection
service.close()
```

## Database Schema

The climate data is stored in the `climate_db.city_climate` collection with the following structure:

```json
{
    "city": "City Name",
    "temperature": {
        "min": 10,
        "max": 25,
        "avg": 17.5
    },
    "precipitation": {
        "annual": 1200,
        "unit": "mm"
    },
    "humidity": {
        "avg": 65,
        "unit": "%"
    },
    "climate_type": "Climate classification",
    "timestamp": "2024-01-01T00:00:00Z"
}
``` 