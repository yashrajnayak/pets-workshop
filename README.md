# Pets workshop

This repository contains the project for two guided workshops to explore various GitHub features. The project is a website for a fictional dog shelter, with a [Flask](https://flask.palletsprojects.com/en/stable/) backend using [MongoDB](https://www.mongodb.com/) and [Astro](https://astro.build/) frontend using [Svelte](https://svelte.dev/) for dynamic pages.

## Architecture

- **Backend**: Flask API with MongoDB database
- **Frontend**: Astro with Svelte components
- **Database**: MongoDB

## Getting started

> **[Get started learning about development with GitHub!](./content/README.md)**

## MongoDB Migration

This project has been converted from using SQLite/SQLAlchemy to MongoDB with PyMongo. The key benefits include:

- **Document-based storage**: More flexible data modeling
- **Aggregation pipelines**: Powerful query capabilities
- **Horizontal scaling**: Better scalability options
- **Cloud-ready**: Easy deployment with MongoDB Atlas

For detailed setup instructions and migration notes, see [server/README_MONGODB.md](./server/README_MONGODB.md).

## Quick Start

1. **Start MongoDB** (using Docker):
   ```bash
   cd server
   docker-compose up -d
   ```

2. **Install dependencies and seed database**:
   ```bash
   cd server
   pip install -r requirements.txt
   python utils/seed_database.py
   ```

3. **Start the application**:
   ```bash
   ./scripts/start-app.sh
   ```

The application will be available at:
- Frontend: http://localhost:4321
- API: http://localhost:5100
- MongoDB Admin (optional): http://localhost:8081

## License 

This project is licensed under the terms of the MIT open source license. Please refer to [MIT](./LICENSE.txt) for the full terms.

## Support

This project is provided as-is, and may be updated over time. If you have questions, please open an issue.
