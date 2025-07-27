#!/usr/bin/env python3
"""
MongoDB Conversion Validation Script

This script validates the MongoDB conversion without requiring a running MongoDB instance.
It tests the model structure and basic functionality using mocks.

NOTE: This is a development/validation script used during the MongoDB migration.
It can be removed in production if not needed, but is useful for:
- Validating the conversion structure
- Testing imports and basic functionality
- Development environment setup validation
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the server directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported correctly"""
    print("Testing imports...")
    
    try:
        from config import Config, DevelopmentConfig
        print("✓ Config modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import config: {e}")
        return False
    
    try:
        from database import MongoDB, db
        print("✓ Database module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import database: {e}")
        return False
    
    try:
        from models.base import BaseModel
        print("✓ BaseModel imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import BaseModel: {e}")
        return False
    
    try:
        from models.breed import Breed
        print("✓ Breed model imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Breed: {e}")
        return False
    
    try:
        from models.dog import Dog, AdoptionStatus
        print("✓ Dog model imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Dog: {e}")
        return False
    
    return True

def test_model_creation():
    """Test model creation and validation"""
    print("\nTesting model creation...")
    
    try:
        from models.breed import Breed
        from models.dog import Dog, AdoptionStatus
        
        # Test Breed creation
        breed = Breed(name="Test Breed", description="A test breed for validation")
        print("✓ Breed model creation successful")
        
        # Test Dog creation
        dog = Dog(
            name="Test Dog",
            age=3,
            gender="Male",
            description="A test dog for validation",
            status=AdoptionStatus.AVAILABLE
        )
        print("✓ Dog model creation successful")
        
        # Test validation
        try:
            invalid_breed = Breed(name="", description="Invalid breed")
        except ValueError:
            print("✓ Breed validation working correctly")
        
        try:
            invalid_dog = Dog(name="", age=3)
        except ValueError:
            print("✓ Dog validation working correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Model creation failed: {e}")
        return False

def test_flask_app():
    """Test Flask app creation (without database connection)"""
    print("\nTesting Flask app...")
    
    try:
        # Mock the database connection to avoid actual MongoDB requirement
        with patch('models.init_db'):
            from app import app
            
            # Test that app is created
            if app:
                print("✓ Flask app created successfully")
                
                # Test that routes are registered
                routes = [rule.rule for rule in app.url_map.iter_rules()]
                expected_routes = ['/api/dogs', '/api/breeds', '/health']
                
                for route in expected_routes:
                    if any(route in r for r in routes):
                        print(f"✓ Route {route} registered")
                    else:
                        print(f"✗ Route {route} not found")
                        return False
                
                return True
            else:
                print("✗ Flask app creation failed")
                return False
                
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
        return False

def test_environment_config():
    """Test environment configuration"""
    print("\nTesting environment configuration...")
    
    try:
        from config import Config, DevelopmentConfig, ProductionConfig
        
        # Test config values
        assert Config.DATABASE_NAME == 'dogshelter'
        print("✓ Database name configuration correct")
        
        assert Config.DOGS_COLLECTION == 'dogs'
        assert Config.BREEDS_COLLECTION == 'breeds'
        print("✓ Collection names configuration correct")
        
        assert DevelopmentConfig.DEBUG == True
        print("✓ Development configuration correct")
        
        assert ProductionConfig.DEBUG == False
        print("✓ Production configuration correct")
        
        return True
        
    except Exception as e:
        print(f"✗ Environment config test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🐕 Pet Shelter MongoDB Conversion Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_model_creation,
        test_environment_config,
        test_flask_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! MongoDB conversion looks good.")
        print("\nNext steps:")
        print("1. Install MongoDB locally or use MongoDB Atlas")
        print("2. Install Python dependencies: pip install -r requirements.txt")
        print("3. Configure .env file with MongoDB connection")
        print("4. Run: python utils/seed_database.py")
        print("5. Run: python app.py")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
