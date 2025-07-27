import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Add the server directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the database initialization before importing app
with patch('database.MongoDB.init_app'):
    from app import app
    from models.dog import AdoptionStatus

class TestApp(unittest.TestCase):
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
        app.config['TESTING'] = True
    
    def _create_mock_dog_document(self, dog_id, name, breed):
        """Helper method to create a mock MongoDB dog document"""
        return {
            '_id': dog_id,
            'name': name,
            'breed': breed,
            'age': 3,
            'gender': 'Male',
            'description': 'A friendly dog',
            'status': AdoptionStatus.AVAILABLE.value
        }
    
    def _create_mock_aggregation_result(self, dogs):
        """Helper method to create mock aggregation pipeline result"""
        return dogs
    
    @patch('models.dog.Dog.find_with_breed_info')
    def test_get_dogs_success(self, mock_find_with_breed):
        """Test successful retrieval of multiple dogs"""
        # Arrange
        mock_dogs = [
            self._create_mock_dog_document("507f1f77bcf86cd799439011", "Buddy", "Labrador"),
            self._create_mock_dog_document("507f1f77bcf86cd799439012", "Max", "German Shepherd")
        ]
        
        mock_find_with_breed.return_value = mock_dogs
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        
        # Verify first dog
        self.assertEqual(data[0]['id'], "507f1f77bcf86cd799439011")
        self.assertEqual(data[0]['name'], "Buddy")
        self.assertEqual(data[0]['breed'], "Labrador")
        
        # Verify second dog
        self.assertEqual(data[1]['id'], "507f1f77bcf86cd799439012")
        self.assertEqual(data[1]['name'], "Max")
        self.assertEqual(data[1]['breed'], "German Shepherd")
        
        # Verify method was called
        mock_find_with_breed.assert_called_once()
    
    @patch('models.dog.Dog.find_with_breed_info')
    def test_get_dogs_empty(self, mock_find_with_breed):
        """Test retrieval when no dogs are available"""
        # Arrange
        mock_find_with_breed.return_value = []
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])
    
    @patch('models.dog.Dog.find_with_breed_info')
    def test_get_dogs_structure(self, mock_find_with_breed):
        """Test the response structure for a single dog"""
        # Arrange
        mock_dog = self._create_mock_dog_document("507f1f77bcf86cd799439011", "Buddy", "Labrador")
        mock_find_with_breed.return_value = [mock_dog]
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)
        self.assertEqual(set(data[0].keys()), {'id', 'name', 'breed'})
    
    @patch('models.dog.Dog.find_by_id_with_breed_info')
    def test_get_dog_success(self, mock_find_by_id):
        """Test successful retrieval of a specific dog"""
        # Arrange
        dog_id = "507f1f77bcf86cd799439011"
        mock_dog = self._create_mock_dog_document(dog_id, "Buddy", "Labrador")
        mock_find_by_id.return_value = mock_dog
        
        # Act
        response = self.app.get(f'/api/dogs/{dog_id}')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['id'], dog_id)
        self.assertEqual(data['name'], "Buddy")
        self.assertEqual(data['breed'], "Labrador")
        self.assertEqual(data['age'], 3)
        self.assertEqual(data['gender'], "Male")
        self.assertEqual(data['description'], "A friendly dog")
        self.assertEqual(data['status'], AdoptionStatus.AVAILABLE.value)
        
        # Verify method was called with correct ID
        mock_find_by_id.assert_called_once_with(dog_id)
    
    @patch('models.dog.Dog.find_by_id_with_breed_info')
    def test_get_dog_not_found(self, mock_find_by_id):
        """Test retrieval of non-existent dog"""
        # Arrange
        dog_id = "507f1f77bcf86cd799439011"
        mock_find_by_id.return_value = None
        
        # Act
        response = self.app.get(f'/api/dogs/{dog_id}')
        
        # Assert
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "Dog not found")
    
    @patch('models.breed.Breed.find_all')
    def test_get_breeds_success(self, mock_find_all):
        """Test successful retrieval of breeds"""
        # Arrange
        mock_breed1 = MagicMock()
        mock_breed1.id = "507f1f77bcf86cd799439013"
        mock_breed1.name = "Labrador"
        mock_breed1.description = "Friendly breed"
        
        mock_breed2 = MagicMock()
        mock_breed2.id = "507f1f77bcf86cd799439014"
        mock_breed2.name = "German Shepherd"
        mock_breed2.description = "Intelligent breed"
        
        mock_find_all.return_value = [mock_breed1, mock_breed2]
        
        # Act
        response = self.app.get('/api/breeds')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        
        # Verify first breed
        self.assertEqual(data[0]['id'], "507f1f77bcf86cd799439013")
        self.assertEqual(data[0]['name'], "Labrador")
        self.assertEqual(data[0]['description'], "Friendly breed")
        
        # Verify second breed
        self.assertEqual(data[1]['id'], "507f1f77bcf86cd799439014")
        self.assertEqual(data[1]['name'], "German Shepherd")
        self.assertEqual(data[1]['description'], "Intelligent breed")
    
    @patch('models.breed.Breed.count')
    @patch('models.dog.Dog.count')
    def test_health_check_success(self, mock_dog_count, mock_breed_count):
        """Test successful health check"""
        # Arrange
        mock_breed_count.return_value = 5
        mock_dog_count.return_value = 20
        
        # Act
        response = self.app.get('/health')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['database'], 'connected')
        self.assertEqual(data['breeds_count'], 5)
        self.assertEqual(data['dogs_count'], 20)

if __name__ == '__main__':
    unittest.main()
