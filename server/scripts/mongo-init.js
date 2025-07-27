// MongoDB initialization script
// This script will run when the MongoDB container starts for the first time

// Create the main database user (if using authentication)
db = db.getSiblingDB('dogshelter');

// Create an index on the breeds collection for unique names
db.breeds.createIndex({ "name": 1 }, { unique: true });

// Create indexes on the dogs collection for better performance
db.dogs.createIndex({ "name": 1 });
db.dogs.createIndex({ "breed_id": 1 });
db.dogs.createIndex({ "status": 1 });
db.dogs.createIndex({ "age": 1 });

print('MongoDB initialization completed for dogshelter database');
