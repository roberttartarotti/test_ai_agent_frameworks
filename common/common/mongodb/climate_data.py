"""MongoDB service for climate data management."""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from common.common.logging_config import get_logger

logger = get_logger("climate_data")


class ClimateDataService:
    """Service for managing climate data in MongoDB."""

    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        """Initialize the climate data service.

        Args:
            connection_string: MongoDB connection string
        """
        self.client = MongoClient(connection_string)
        self.db: Database = self.client["climate_db"]
        self.collection: Collection = self.db["city_climate"]
        self.logger = get_logger("climate_data_service")

    def insert_city_climate(self, city_data: Dict) -> str:
        """Insert climate data for a city.

        Args:
            city_data: Climate data dictionary for the city

        Returns:
            Inserted document ID
        """
        city_data["timestamp"] = datetime.now()
        result = self.collection.insert_one(city_data)
        self.logger.info(f"Inserted climate data for {city_data.get('city', 'Unknown')}")
        return str(result.inserted_id)

    def get_city_climate(self, city_name: str) -> Optional[Dict]:
        """Get climate data for a specific city.

        Args:
            city_name: Name of the city

        Returns:
            Climate data dictionary or None if not found
        """
        data = self.collection.find_one({"city": city_name})
        if data:
            self.logger.info(f"Retrieved climate data for {city_name}")
        else:
            self.logger.warning(f"No climate data found for {city_name}")
        return data

    def get_all_cities(self) -> List[str]:
        """Get list of all cities with climate data.

        Returns:
            List of city names
        """
        cities = self.collection.distinct("city")
        self.logger.info(f"Retrieved {len(cities)} cities with climate data")
        return cities

    def update_city_climate(self, city_name: str, climate_data: Dict) -> bool:
        """Update climate data for a city.

        Args:
            city_name: Name of the city
            climate_data: Updated climate data

        Returns:
            True if update was successful, False otherwise
        """
        climate_data["timestamp"] = datetime.now()
        result = self.collection.update_one(
            {"city": city_name}, {"$set": climate_data}, upsert=True
        )
        success = result.modified_count > 0 or result.upserted_id is not None
        if success:
            self.logger.info(f"Updated climate data for {city_name}")
        else:
            self.logger.warning(f"Failed to update climate data for {city_name}")
        return success

    def delete_city_climate(self, city_name: str) -> bool:
        """Delete climate data for a city.

        Args:
            city_name: Name of the city

        Returns:
            True if deletion was successful, False otherwise
        """
        result = self.collection.delete_one({"city": city_name})
        success = result.deleted_count > 0
        if success:
            self.logger.info(f"Deleted climate data for {city_name}")
        else:
            self.logger.warning(f"No climate data found to delete for {city_name}")
        return success

    def get_climate_statistics(self) -> Dict:
        """Get climate database statistics.

        Returns:
            Dictionary containing database statistics
        """
        total_cities = self.collection.count_documents({})
        latest_update = self.collection.find_one(
            sort=[("timestamp", -1)]
        )
        
        stats = {
            "total_cities": total_cities,
            "latest_update": latest_update.get("timestamp") if latest_update else None,
            "database_name": self.db.name,
            "collection_name": self.collection.name,
        }
        
        self.logger.info(f"Retrieved database statistics: {stats}")
        return stats

    def close(self) -> None:
        """Close the MongoDB connection."""
        self.client.close()
        self.logger.info("MongoDB connection closed") 