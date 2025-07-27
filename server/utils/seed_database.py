import csv
import os
import sys
import random
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from bson import ObjectId

# Add the parent directory to sys.path to allow importing from models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import init_db, Breed, Dog
from models.dog import AdoptionStatus
from config import DevelopmentConfig

# Configure logging
logging.basicConfig(level=logging.INFO)

def seed_breeds():
    """Seed the database with breeds from the CSV file"""
    
    # Path to the CSV file
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           'models', 'breeds.csv')
    
    # Check if breeds already exist
    existing_breeds_count = Breed.count()
    if existing_breeds_count > 0:
        logging.info(f"Database already contains {existing_breeds_count} breeds. Skipping seed.")
        return
    
    # Read the CSV file and add breeds to the database
    breeds_added = 0
    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            try:
                breed = Breed(name=row['Breed'], description=row['Description'])
                breed.save()
                breeds_added += 1
            except Exception as e:
                logging.error(f"Error adding breed {row['Breed']}: {e}")
    
    logging.info(f"Successfully seeded {breeds_added} breeds to the database.")

def seed_dogs():
    """Seed the database with dogs from the CSV file, ensuring at least 3 dogs per breed"""
    
    # Path to the CSV file
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           'models', 'dogs.csv')
    
    # Check if dogs already exist
    existing_dogs_count = Dog.count()
    if existing_dogs_count > 0:
        logging.info(f"Database already contains {existing_dogs_count} dogs. Skipping seed.")
        return
    
    # Get all breeds from the database
    breeds = Breed.find_all()
    if not breeds:
        logging.error("No breeds found in database. Please seed breeds first.")
        return
    
    # Track how many dogs are assigned to each breed
    breed_counts = defaultdict(int)
    
    # Read the CSV file
    dogs_data = []
    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            dogs_data.append(row)
    
    def create_dog(dog_info, breed):
        """Helper function to create a dog with consistent attributes"""
        try:
            dog = Dog(
                name=dog_info['Name'],
                description=dog_info['Description'],
                breed_id=breed._id,
                age=int(dog_info['Age']),
                gender=dog_info['Gender'],
                status=random.choice(list(AdoptionStatus)),
                intake_date=datetime.utcnow() - timedelta(days=random.randint(1, 365))
            )
            dog.save()
            breed_counts[breed.id] += 1
            return dog
        except Exception as e:
            logging.error(f"Error creating dog {dog_info['Name']}: {e}")
            return None
    
    dogs_added = 0
    
    # First pass: assign at least 3 dogs to each breed
    for breed in breeds:
        # Get 3 random dogs that haven't been assigned yet
        for _ in range(3):
            if not dogs_data:
                break
            
            dog_info = random.choice(dogs_data)
            dogs_data.remove(dog_info)
            
            dog = create_dog(dog_info, breed)
            if dog:
                dogs_added += 1
    
    # Second pass: assign remaining dogs randomly
    for dog_info in dogs_data:
        breed = random.choice(breeds)
        dog = create_dog(dog_info, breed)
        if dog:
            dogs_added += 1
    
    logging.info(f"Successfully seeded {dogs_added} dogs to the database.")
    
    # Print distribution of dogs across breeds
    for breed in breeds:
        count = breed_counts[breed.id]
        logging.info(f"Breed '{breed.name}': {count} dogs")

def seed_database():
    """Run all seeding functions in the correct order"""
    try:
        # Initialize database connection
        init_db(DevelopmentConfig)
        
        logging.info("Starting database seeding...")
        seed_breeds()
        seed_dogs()
        logging.info("Database seeding completed successfully!")
        
    except Exception as e:
        logging.error(f"Error during database seeding: {e}")
        raise

if __name__ == '__main__':
    seed_database()