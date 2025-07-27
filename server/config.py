import os
from typing import Optional

class Config:
    """Configuration class for MongoDB connection and app settings"""
    
    # MongoDB configuration
    MONGODB_URI: str = os.getenv(
        'MONGODB_URI', 
        'mongodb://localhost:27017/'  # Default local MongoDB
    )
    DATABASE_NAME: str = os.getenv('DATABASE_NAME', 'dogshelter')
    
    # Collection names
    DOGS_COLLECTION: str = 'dogs'
    BREEDS_COLLECTION: str = 'breeds'
    
    # Flask configuration
    DEBUG: bool = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    PORT: int = int(os.getenv('FLASK_PORT', '5100'))
    
    @classmethod
    def get_mongodb_uri(cls) -> str:
        """Get the complete MongoDB URI"""
        return cls.MONGODB_URI
    
    @classmethod
    def get_database_name(cls) -> str:
        """Get the database name"""
        return cls.DATABASE_NAME

# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    DATABASE_NAME = 'dogshelter_test'
    DEBUG = True

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
