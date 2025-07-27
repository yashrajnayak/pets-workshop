from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Optional
import logging

from config import Config

class MongoDB:
    """MongoDB connection manager"""
    
    def __init__(self):
        self._client: Optional[MongoClient] = None
        self._database: Optional[Database] = None
        
    def init_app(self, config: Config = None):
        """Initialize MongoDB connection"""
        if config is None:
            config = Config()
            
        try:
            self._client = MongoClient(config.get_mongodb_uri())
            self._database = self._client[config.get_database_name()]
            
            # Test the connection
            self._client.admin.command('ping')
            logging.info(f"Successfully connected to MongoDB: {config.get_database_name()}")
            
            # Create indexes for better performance
            self._create_indexes()
            
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def _create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # Index for dogs collection
            dogs_collection = self.get_collection(Config.DOGS_COLLECTION)
            dogs_collection.create_index([("name", 1)])
            dogs_collection.create_index([("breed_id", 1)])
            dogs_collection.create_index([("status", 1)])
            dogs_collection.create_index([("age", 1)])
            
            # Index for breeds collection
            breeds_collection = self.get_collection(Config.BREEDS_COLLECTION)
            breeds_collection.create_index([("name", 1)], unique=True)
            
            logging.info("Database indexes created successfully")
            
        except Exception as e:
            logging.warning(f"Failed to create indexes: {e}")
    
    def get_database(self) -> Database:
        """Get the database instance"""
        if self._database is None:
            raise RuntimeError("Database not initialized. Call init_app() first.")
        return self._database
    
    def get_collection(self, collection_name: str) -> Collection:
        """Get a collection from the database"""
        return self.get_database()[collection_name]
    
    def close_connection(self):
        """Close the MongoDB connection"""
        if self._client:
            self._client.close()
            logging.info("MongoDB connection closed")

# Global MongoDB instance
db = MongoDB()

def init_db(config: Config = None):
    """Initialize the database connection"""
    db.init_app(config)
