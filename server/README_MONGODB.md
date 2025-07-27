# Pet Shelter API - MongoDB Version

This is the MongoDB version of the Pet Shelter API, converted from the original SQLite/SQLAlchemy implementation.

## Changes Made

### Database Migration
- **Database**: Migrated from SQLite to MongoDB
- **ORM**: Removed SQLAlchemy, implemented custom MongoDB models using PyMongo
- **Schema**: Converted relational data model to document-based model

### Key Improvements
1. **Document-based Storage**: Leverage MongoDB's flexible document structure
2. **Aggregation Pipelines**: Use MongoDB's powerful aggregation for complex queries
3. **Scalability**: Better horizontal scaling capabilities
4. **Performance**: Optimized indexes for common query patterns

## Setup Instructions

### Prerequisites
- Python 3.8+
- MongoDB 7.0+ (local installation or Docker)
- pip (Python package manager)

### Local Development Setup

#### Option 1: Using Local MongoDB
1. Install MongoDB locally (https://docs.mongodb.com/manual/installation/)
2. Start MongoDB service:
   ```bash
   # macOS with Homebrew
   brew services start mongodb/brew/mongodb-community
   
   # Linux with systemd
   sudo systemctl start mongod
   
   # Windows
   net start MongoDB
   ```

#### Option 2: Using Docker (Recommended)
1. Start MongoDB using Docker Compose:
   ```bash
   cd server
   docker-compose up -d
   ```
   This will start:
   - MongoDB on port 27017
   - MongoDB Express (web admin) on port 8081

### Application Setup

1. **Install Dependencies**:
   ```bash
   cd server
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file with your MongoDB connection details
   # For local MongoDB:
   MONGODB_URI=mongodb://localhost:27017/
   DATABASE_NAME=dogshelter
   ```

3. **Seed the Database**:
   ```bash
   python utils/seed_database.py
   ```

4. **Start the Application**:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5100`

## Database Schema

### Breeds Collection
```javascript
{
  "_id": ObjectId("..."),
  "name": "Labrador Retriever",
  "description": "America's favorite family dog, friendly and easy-going.",
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

### Dogs Collection
```javascript
{
  "_id": ObjectId("..."),
  "name": "Buddy",
  "breed_id": ObjectId("..."), // Reference to breeds collection
  "age": 3,
  "gender": "Male",
  "description": "A friendly and energetic dog...",
  "status": "Available", // Available, Adopted, Pending
  "intake_date": ISODate("..."),
  "adoption_date": ISODate("..."), // null if not adopted
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

## API Endpoints

### Dogs
- `GET /api/dogs` - Get all dogs with breed information
- `GET /api/dogs/{id}` - Get specific dog details with breed information

### Breeds
- `GET /api/breeds` - Get all breeds

### Health Check
- `GET /health` - API and database health status

## Features

### MongoDB Aggregation Pipeline
The application uses MongoDB's aggregation pipeline for complex queries:
- **Lookup Operations**: Join dogs with breeds data
- **Projection**: Select only required fields
- **Sorting**: Efficient sorting with indexes

### Indexing Strategy
Optimized indexes for common query patterns:
- Breeds: `name` (unique index)
- Dogs: `name`, `breed_id`, `status`, `age`

### Error Handling
- Comprehensive error handling for database operations
- Proper HTTP status codes
- Detailed error logging

## Testing

Run the updated tests:
```bash
python test_app_mongodb.py
```

The tests use mocking to avoid requiring a real database connection.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/` |
| `DATABASE_NAME` | Database name | `dogshelter` |
| `FLASK_ENV` | Flask environment | `development` |
| `FLASK_DEBUG` | Enable debug mode | `True` |
| `FLASK_PORT` | Flask port | `5100` |

## MongoDB Atlas (Cloud) Setup

To use MongoDB Atlas instead of local MongoDB:

1. Create an account at https://www.mongodb.com/atlas
2. Create a cluster
3. Get your connection string
4. Update your `.env` file:
   ```bash
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/<database-name>?retryWrites=true&w=majority
   DATABASE_NAME=dogshelter
   ```

## Performance Considerations

### Indexes
- All collections have appropriate indexes for common queries
- Compound indexes can be added for more complex query patterns

### Connection Pooling
- PyMongo automatically handles connection pooling
- Default pool size is usually sufficient for most applications

### Aggregation Optimization
- Aggregation pipelines are optimized to use indexes where possible
- `$match` stages are placed early in the pipeline

## Migration Notes

### Data Migration
- Breed IDs are now ObjectIds instead of integers
- All timestamps are stored as ISODate objects
- Status values remain as strings but are validated using Python enums

### API Compatibility
- All existing API endpoints maintain the same interface
- Response formats are identical to the original SQLite version
- Dog/Breed IDs are returned as strings (ObjectId string representation)

## Troubleshooting

### Common Issues

1. **Connection Refused**:
   - Ensure MongoDB is running
   - Check the connection string in `.env`

2. **Authentication Failed**:
   - Verify username/password in connection string
   - Check database permissions

3. **Import Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python path configuration

### Logs
The application logs important events and errors. Check the console output for detailed information about database operations and any issues.
