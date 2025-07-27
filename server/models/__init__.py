from database import db, init_db

# Import models after db is defined to avoid circular imports
from .breed import Breed
from .dog import Dog

__all__ = ['db', 'init_db', 'Breed', 'Dog']