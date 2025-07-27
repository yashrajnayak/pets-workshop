from typing import Dict, Any, List, Optional
from bson import ObjectId
from database import db
from config import Config
from .base import BaseModel

class Breed(BaseModel):
    """Breed model for MongoDB"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name: str = kwargs.get('name', '')
        self.description: Optional[str] = kwargs.get('description')
        
        # Validate the data
        self._validate()
    
    def _validate(self):
        """Validate breed data"""
        self.name = self.validate_string_length('Breed name', self.name, min_length=2)
        if self.description is not None:
            self.description = self.validate_string_length(
                'Description', self.description, min_length=10, allow_none=True
            )
    
    def save(self) -> 'Breed':
        """Save the breed to the database"""
        self._validate()
        self.update_timestamp()
        
        collection = db.get_collection(Config.BREEDS_COLLECTION)
        
        if self._id:
            # Update existing breed
            result = collection.update_one(
                {'_id': self._id},
                {'$set': self.to_dict(include_id=False)}
            )
            if result.modified_count == 0:
                raise ValueError("Breed not found or no changes made")
        else:
            # Insert new breed
            result = collection.insert_one(self.to_dict(include_id=False))
            self._id = result.inserted_id
        
        return self
    
    def delete(self) -> bool:
        """Delete the breed from the database"""
        if not self._id:
            return False
        
        collection = db.get_collection(Config.BREEDS_COLLECTION)
        result = collection.delete_one({'_id': self._id})
        return result.deleted_count > 0
    
    @classmethod
    def find_by_id(cls, breed_id: str) -> Optional['Breed']:
        """Find a breed by ID"""
        try:
            object_id = ObjectId(breed_id)
            collection = db.get_collection(Config.BREEDS_COLLECTION)
            doc = collection.find_one({'_id': object_id})
            
            if doc:
                return cls.from_dict(doc)
            return None
        except Exception:
            return None
    
    @classmethod
    def find_by_name(cls, name: str) -> Optional['Breed']:
        """Find a breed by name"""
        collection = db.get_collection(Config.BREEDS_COLLECTION)
        doc = collection.find_one({'name': {'$regex': f'^{name}$', '$options': 'i'}})
        
        if doc:
            return cls.from_dict(doc)
        return None
    
    @classmethod
    def find_all(cls) -> List['Breed']:
        """Find all breeds"""
        collection = db.get_collection(Config.BREEDS_COLLECTION)
        docs = collection.find().sort('name', 1)
        
        return [cls.from_dict(doc) for doc in docs]
    
    @classmethod
    def count(cls) -> int:
        """Count total number of breeds"""
        collection = db.get_collection(Config.BREEDS_COLLECTION)
        return collection.count_documents({})
    
    def to_dict(self, include_id: bool = True) -> Dict[str, Any]:
        """Convert breed to dictionary"""
        result = super().to_dict(include_id)
        result.update({
            'name': self.name,
            'description': self.description
        })
        return result
    
    def __repr__(self):
        return f'<Breed {self.name}>'