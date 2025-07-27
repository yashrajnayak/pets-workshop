from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional
from bson import ObjectId
from database import db
from config import Config
from .base import BaseModel

# Define an Enum for dog status
class AdoptionStatus(Enum):
    AVAILABLE = 'Available'
    ADOPTED = 'Adopted'
    PENDING = 'Pending'

class Dog(BaseModel):
    """Dog model for MongoDB"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name: str = kwargs.get('name', '')
        self.breed_id: Optional[str] = kwargs.get('breed_id')
        self.age: Optional[int] = kwargs.get('age')
        self.gender: Optional[str] = kwargs.get('gender')
        self.description: Optional[str] = kwargs.get('description')
        
        # Adoption status
        status_value = kwargs.get('status', AdoptionStatus.AVAILABLE)
        if isinstance(status_value, str):
            # Handle string values (e.g., from database)
            try:
                self.status = AdoptionStatus(status_value)
            except ValueError:
                # Handle enum name format (e.g., 'AVAILABLE')
                self.status = AdoptionStatus[status_value]
        else:
            self.status = status_value
            
        self.intake_date: datetime = kwargs.get('intake_date', datetime.utcnow())
        self.adoption_date: Optional[datetime] = kwargs.get('adoption_date')
        
        # Validate the data
        self._validate()
    
    def _validate(self):
        """Validate dog data"""
        self.name = self.validate_string_length('Dog name', self.name, min_length=2)
        
        if self.gender and self.gender not in ['Male', 'Female', 'Unknown']:
            raise ValueError("Gender must be 'Male', 'Female', or 'Unknown'")
        
        if self.description is not None:
            self.description = self.validate_string_length(
                'Description', self.description, min_length=10, allow_none=True
            )
    
    def save(self) -> 'Dog':
        """Save the dog to the database"""
        self._validate()
        self.update_timestamp()
        
        collection = db.get_collection(Config.DOGS_COLLECTION)
        
        # Convert ObjectId breed_id to string if needed
        doc_data = self.to_dict(include_id=False)
        
        if self._id:
            # Update existing dog
            result = collection.update_one(
                {'_id': self._id},
                {'$set': doc_data}
            )
            if result.modified_count == 0:
                raise ValueError("Dog not found or no changes made")
        else:
            # Insert new dog
            result = collection.insert_one(doc_data)
            self._id = result.inserted_id
        
        return self
    
    def delete(self) -> bool:
        """Delete the dog from the database"""
        if not self._id:
            return False
        
        collection = db.get_collection(Config.DOGS_COLLECTION)
        result = collection.delete_one({'_id': self._id})
        return result.deleted_count > 0
    
    @classmethod
    def find_by_id(cls, dog_id: str) -> Optional['Dog']:
        """Find a dog by ID"""
        try:
            object_id = ObjectId(dog_id)
            collection = db.get_collection(Config.DOGS_COLLECTION)
            doc = collection.find_one({'_id': object_id})
            
            if doc:
                return cls.from_dict(doc)
            return None
        except Exception:
            return None
    
    @classmethod
    def find_all(cls) -> List['Dog']:
        """Find all dogs"""
        collection = db.get_collection(Config.DOGS_COLLECTION)
        docs = collection.find().sort('name', 1)
        
        return [cls.from_dict(doc) for doc in docs]
    
    @classmethod
    def find_with_breed_info(cls) -> List[Dict[str, Any]]:
        """Find all dogs with breed information using aggregation"""
        collection = db.get_collection(Config.DOGS_COLLECTION)
        
        pipeline = [
            {
                '$lookup': {
                    'from': Config.BREEDS_COLLECTION,
                    'localField': 'breed_id',
                    'foreignField': '_id',
                    'as': 'breed_info'
                }
            },
            {
                '$unwind': {
                    'path': '$breed_info',
                    'preserveNullAndEmptyArrays': True
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'breed': '$breed_info.name',
                    'age': 1,
                    'gender': 1,
                    'description': 1,
                    'status': 1,
                    'intake_date': 1,
                    'adoption_date': 1
                }
            },
            {
                '$sort': {'name': 1}
            }
        ]
        
        return list(collection.aggregate(pipeline))
    
    @classmethod
    def find_by_id_with_breed_info(cls, dog_id: str) -> Optional[Dict[str, Any]]:
        """Find a dog by ID with breed information"""
        try:
            object_id = ObjectId(dog_id)
            collection = db.get_collection(Config.DOGS_COLLECTION)
            
            pipeline = [
                {
                    '$match': {'_id': object_id}
                },
                {
                    '$lookup': {
                        'from': Config.BREEDS_COLLECTION,
                        'localField': 'breed_id',
                        'foreignField': '_id',
                        'as': 'breed_info'
                    }
                },
                {
                    '$unwind': {
                        'path': '$breed_info',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                {
                    '$project': {
                        '_id': 1,
                        'name': 1,
                        'breed': '$breed_info.name',
                        'age': 1,
                        'gender': 1,
                        'description': 1,
                        'status': 1,
                        'intake_date': 1,
                        'adoption_date': 1
                    }
                }
            ]
            
            result = list(collection.aggregate(pipeline))
            return result[0] if result else None
            
        except Exception:
            return None
    
    @classmethod
    def find_by_breed_id(cls, breed_id: str) -> List['Dog']:
        """Find all dogs of a specific breed"""
        try:
            object_id = ObjectId(breed_id)
            collection = db.get_collection(Config.DOGS_COLLECTION)
            docs = collection.find({'breed_id': object_id}).sort('name', 1)
            
            return [cls.from_dict(doc) for doc in docs]
        except Exception:
            return []
    
    @classmethod
    def count(cls) -> int:
        """Count total number of dogs"""
        collection = db.get_collection(Config.DOGS_COLLECTION)
        return collection.count_documents({})
    
    def to_dict(self, include_id: bool = True) -> Dict[str, Any]:
        """Convert dog to dictionary"""
        result = super().to_dict(include_id)
        result.update({
            'name': self.name,
            'breed_id': str(self.breed_id) if self.breed_id else None,
            'age': self.age,
            'gender': self.gender,
            'description': self.description,
            'status': self.status.value if self.status else None,
            'intake_date': self.intake_date.isoformat() if self.intake_date else None,
            'adoption_date': self.adoption_date.isoformat() if self.adoption_date else None
        })
        return result
    
    def __repr__(self):
        return f'<Dog {self.name}, ID: {self.id}, Status: {self.status.value if self.status else "Unknown"}>'