"""Tools for CrewAI agent to interact with MongoDB temperature data."""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from common.common.mongodb.climate_data import ClimateDataService
from common.common.logging_config import get_logger


class TemperatureData(BaseModel):
    """Temperature data model for cities."""
    
    city: str = Field(description="Name of the city")
    temperature_celsius: float = Field(description="Temperature in Celsius")
    humidity_percent: float = Field(description="Humidity percentage")
    weather_condition: str = Field(description="Weather condition (sunny, cloudy, rainy, etc.)")
    timestamp: datetime = Field(description="Timestamp of the measurement")


class TemperatureTools:
    """Tools for managing temperature data in MongoDB."""

    def __init__(self):
        """Initialize temperature tools and sample data."""
        self.climate_service = ClimateDataService()
        self.logger = get_logger("temperature_tools")
        self._initialize_sample_data()

    def _initialize_sample_data(self) -> None:
        """Initialize sample temperature data for predefined cities."""
        sample_cities = [
            "San Francisco", "New York", "London", "Tokyo", "Paris", 
            "Sydney", "Rio de Janeiro", "Moscow", "Cairo", "Mumbai",
            "São Paulo", "Mexico City", "Toronto", "Berlin", "Madrid"
        ]
        
        for city in sample_cities:
            existing_data = self.climate_service.get_city_climate(city)
            if not existing_data:
                self._generate_sample_data_for_city(city)

    def _generate_sample_data_for_city(self, city: str) -> None:
        """Generate sample temperature data for a specific city.

        Args:
            city: Name of the city
        """
        base_temps = {
            "San Francisco": (12, 18),
            "New York": (5, 25),
            "London": (8, 20),
            "Tokyo": (10, 28),
            "Paris": (7, 22),
            "Sydney": (15, 30),
            "Rio de Janeiro": (20, 35),
            "Moscow": (-5, 20),
            "Cairo": (15, 35),
            "Mumbai": (20, 38),
            "São Paulo": (15, 28),
            "Mexico City": (12, 25),
            "Toronto": (0, 22),
            "Berlin": (5, 20),
            "Madrid": (8, 28)
        }
        
        min_temp, max_temp = base_temps.get(city, (10, 25))
        current_temp = random.uniform(min_temp, max_temp)
        humidity = random.uniform(40, 80)
        conditions = ["sunny", "cloudy", "partly cloudy", "rainy", "foggy"]
        weather = random.choice(conditions)
        
        temperature_data = {
            "city": city,
            "temperature_celsius": round(current_temp, 1),
            "humidity_percent": round(humidity, 1),
            "weather_condition": weather,
            "timestamp": datetime.now(),
            "climate_type": self._get_climate_type(city, current_temp),
            "seasonal_info": self._get_seasonal_info(city)
        }
        
        self.climate_service.insert_city_climate(temperature_data)

    def _get_climate_type(self, city: str, temp: float) -> str:
        """Get climate type based on temperature.

        Args:
            city: Name of the city
            temp: Temperature in Celsius

        Returns:
            Climate type string
        """
        if temp < 0:
            return "Cold"
        elif temp < 15:
            return "Cool"
        elif temp < 25:
            return "Mild"
        else:
            return "Warm"

    def _get_seasonal_info(self, city: str) -> Dict:
        """Get seasonal information for a city.

        Args:
            city: Name of the city

        Returns:
            Dictionary with seasonal information
        """
        seasons = {
            "San Francisco": {"current": "Summer", "description": "Cool summers with fog"},
            "New York": {"current": "Summer", "description": "Hot summers, cold winters"},
            "London": {"current": "Summer", "description": "Mild summers, rainy winters"},
            "Tokyo": {"current": "Summer", "description": "Hot humid summers, mild winters"},
            "Paris": {"current": "Summer", "description": "Mild summers, cool winters"}
        }
        return seasons.get(city, {"current": "Summer", "description": "Temperate climate"})

    def get_current_temperature(self, city: str) -> Dict:
        """Get current temperature data for a city.

        Args:
            city: Name of the city

        Returns:
            Dictionary with temperature information
        """
        data = self.climate_service.get_city_climate(city)
        if data:
            return {
                "city": data["city"],
                "temperature": f"{data['temperature_celsius']}°C",
                "humidity": f"{data['humidity_percent']}%",
                "weather": data["weather_condition"],
                "timestamp": data["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {"error": f"No temperature data found for {city}"}

    def get_temperature_comparison(self, city1: str, city2: str) -> Dict:
        """Compare temperatures between two cities.

        Args:
            city1: Name of the first city
            city2: Name of the second city

        Returns:
            Dictionary with temperature comparison data
        """
        data1 = self.climate_service.get_city_climate(city1)
        data2 = self.climate_service.get_city_climate(city2)
        
        if data1 and data2:
            temp_diff = data1["temperature_celsius"] - data2["temperature_celsius"]
            return {
                "city1": {
                    "name": city1,
                    "temperature": f"{data1['temperature_celsius']}°C",
                    "weather": data1["weather_condition"]
                },
                "city2": {
                    "name": city2,
                    "temperature": f"{data2['temperature_celsius']}°C",
                    "weather": data2["weather_condition"]
                },
                "difference": f"{abs(temp_diff):.1f}°C",
                "warmer_city": city1 if temp_diff > 0 else city2
            }
        else:
            return {"error": "Could not retrieve temperature data for one or both cities"}

    def get_all_cities_temperatures(self) -> List[Dict]:
        """Get temperature data for all cities.

        Returns:
            List of dictionaries with temperature data for each city
        """
        cities = self.climate_service.get_all_cities()
        temperatures = []
        
        for city in cities:
            data = self.climate_service.get_city_climate(city)
            if data:
                temperatures.append({
                    "city": city,
                    "temperature": f"{data['temperature_celsius']}°C",
                    "weather": data["weather_condition"]
                })
        
        return sorted(temperatures, key=lambda x: x["city"])

    def update_city_temperature(self, city: str, temperature: float, humidity: float, weather: str) -> Dict:
        """Update temperature data for a city.

        Args:
            city: Name of the city
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            weather: Weather condition

        Returns:
            Dictionary with update result
        """
        temperature_data = {
            "city": city,
            "temperature_celsius": temperature,
            "humidity_percent": humidity,
            "weather_condition": weather,
            "timestamp": datetime.now(),
            "climate_type": self._get_climate_type(city, temperature),
            "seasonal_info": self._get_seasonal_info(city)
        }
        
        success = self.climate_service.update_city_climate(city, temperature_data)
        if success:
            return {"success": True, "message": f"Updated temperature for {city}"}
        else:
            return {"success": False, "message": f"Failed to update temperature for {city}"}

    def get_weather_summary(self) -> Dict:
        """Get weather summary for all cities.

        Returns:
            Dictionary with weather summary statistics
        """
        cities = self.climate_service.get_all_cities()
        total_cities = len(cities)
        temperatures = []
        weather_conditions = {}
        
        for city in cities:
            data = self.climate_service.get_city_climate(city)
            if data:
                temperatures.append(data["temperature_celsius"])
                weather = data["weather_condition"]
                weather_conditions[weather] = weather_conditions.get(weather, 0) + 1
        
        if temperatures:
            avg_temp = sum(temperatures) / len(temperatures)
            hottest_city = max(cities, key=lambda c: self.climate_service.get_city_climate(c)["temperature_celsius"] if self.climate_service.get_city_climate(c) else 0)
            coldest_city = min(cities, key=lambda c: self.climate_service.get_city_climate(c)["temperature_celsius"] if self.climate_service.get_city_climate(c) else 0)
            
            return {
                "total_cities": total_cities,
                "average_temperature": f"{avg_temp:.1f}°C",
                "hottest_city": hottest_city,
                "coldest_city": coldest_city,
                "weather_distribution": weather_conditions
            }
        else:
            return {"error": "No temperature data available"}

    def close(self) -> None:
        """Close the temperature tools and database connection."""
        self.climate_service.close()
        self.logger.info("Temperature tools closed") 