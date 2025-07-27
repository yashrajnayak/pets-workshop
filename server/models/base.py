from typing import Dict, Any, Optional
from bson import ObjectId
from datetime import datetime

class BaseModel:
    """Base model class for MongoDB documents"""
    
    def __init__(self, **kwargs):
        """Initialize the model with provided data"""
        self._id: Optional[ObjectId] = kwargs.get('_id')
        self.created_at: datetime = kwargs.get('created_at', datetime.utcnow())
        self.updated_at: datetime = kwargs.get('updated_at', datetime.utcnow())
    
    @property
    def id(self) -> str:
        """Get the document ID as a string"""
        return str(self._id) if self._id else None
    
    def to_dict(self, include_id: bool = True) -> Dict[str, Any]:
        """Convert the model to a dictionary"""
        result = {}
        
        for key, value in self.__dict__.items():
            if key.startswith('_') and key != '_id':
                continue
                
            if key == '_id':
                if include_id and value:
                    result['id'] = str(value)
            elif isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
                
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create a model instance from a dictionary"""
        return cls(**data)
    
    @staticmethod
    def validate_string_length(field_name: str, value: Any, min_length: int = 2, allow_none: bool = False) -> str:
        """Validate string field length"""
        if value is None:
            if allow_none:
                return value
            else:
                raise ValueError(f"{field_name} cannot be empty")
        
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
            
        if len(value.strip()) < min_length:
            raise ValueError(f"{field_name} must be at least {min_length} characters")
            
        return value.strip()
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()