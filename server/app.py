import os
import logging
from typing import Dict, List, Any, Optional
from flask import Flask, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv

from models import init_db, Dog, Breed
from config import Config, config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get the server directory path
base_dir: str = os.path.abspath(os.path.dirname(__file__))

app: Flask = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Get environment and configure app
env = os.getenv('FLASK_ENV', 'development')
app_config = config.get(env, config['default'])

# Initialize the database
init_db(app_config)

@app.route('/api/dogs', methods=['GET'])
def get_dogs() -> Response:
    """Get all dogs with breed information"""
    try:
        # Use aggregation to get dogs with breed names
        dogs_data = Dog.find_with_breed_info()
        
        # Convert the result to a list of dictionaries with proper formatting
        dogs_list: List[Dict[str, Any]] = []
        for dog_data in dogs_data:
            dogs_list.append({
                'id': str(dog_data['_id']),
                'name': dog_data['name'],
                'breed': dog_data.get('breed', 'Unknown')
            })
        
        return jsonify(dogs_list)
    
    except Exception as e:
        logging.error(f"Error retrieving dogs: {e}")
        return jsonify({"error": "Failed to retrieve dogs"}), 500

@app.route('/api/dogs/<dog_id>', methods=['GET'])
def get_dog(dog_id: str) -> tuple[Response, int] | Response:
    """Get a specific dog by ID with breed information"""
    try:
        # Find dog by ID with breed information
        dog_data = Dog.find_by_id_with_breed_info(dog_id)
        
        # Return 404 if dog not found
        if not dog_data:
            return jsonify({"error": "Dog not found"}), 404
        
        # Convert the result to a properly formatted dictionary
        dog: Dict[str, Any] = {
            'id': str(dog_data['_id']),
            'name': dog_data['name'],
            'breed': dog_data.get('breed', 'Unknown'),
            'age': dog_data.get('age'),
            'description': dog_data.get('description'),
            'gender': dog_data.get('gender'),
            'status': dog_data.get('status', 'AVAILABLE')
        }
        
        return jsonify(dog)
    
    except Exception as e:
        logging.error(f"Error retrieving dog {dog_id}: {e}")
        return jsonify({"error": "Failed to retrieve dog"}), 500

@app.route('/api/breeds', methods=['GET'])
def get_breeds() -> Response:
    """Get all breeds"""
    try:
        breeds = Breed.find_all()
        
        breeds_list: List[Dict[str, Any]] = []
        for breed in breeds:
            breeds_list.append({
                'id': breed.id,
                'name': breed.name,
                'description': breed.description
            })
        
        return jsonify(breeds_list)
    
    except Exception as e:
        logging.error(f"Error retrieving breeds: {e}")
        return jsonify({"error": "Failed to retrieve breeds"}), 500

@app.route('/health', methods=['GET'])
def health_check() -> Response:
    """Health check endpoint"""
    try:
        # Test database connection
        breeds_count = Breed.count()
        dogs_count = Dog.count()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "breeds_count": breeds_count,
            "dogs_count": dogs_count
        })
    
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=app_config.DEBUG, port=app_config.PORT)