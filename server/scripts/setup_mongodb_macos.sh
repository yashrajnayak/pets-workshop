#!/bin/bash

# MongoDB Setup Script for macOS
# This script helps set up MongoDB for local development

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}MongoDB Setup for Pet Shelter API${NC}"
echo "================================="

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo -e "${RED}Homebrew is not installed. Please install Homebrew first:${NC}"
    echo "Visit: https://brew.sh/"
    exit 1
fi

# Check if MongoDB is already installed
if command -v mongod &> /dev/null; then
    echo -e "${GREEN}MongoDB is already installed.${NC}"
else
    echo -e "${YELLOW}Installing MongoDB Community Edition...${NC}"
    
    # Add MongoDB tap
    brew tap mongodb/brew
    
    # Install MongoDB
    brew install mongodb-community
    
    echo -e "${GREEN}MongoDB installed successfully!${NC}"
fi

# Check if MongoDB is running
if pgrep mongod > /dev/null; then
    echo -e "${GREEN}MongoDB is already running.${NC}"
else
    echo -e "${YELLOW}Starting MongoDB...${NC}"
    
    # Start MongoDB as a service
    brew services start mongodb/brew/mongodb-community
    
    # Wait a moment for MongoDB to start
    sleep 3
    
    if pgrep mongod > /dev/null; then
        echo -e "${GREEN}MongoDB started successfully!${NC}"
    else
        echo -e "${RED}Failed to start MongoDB. Please check the logs.${NC}"
        exit 1
    fi
fi

# Test MongoDB connection
echo -e "${YELLOW}Testing MongoDB connection...${NC}"
if mongosh --eval "db.runCommand('ping')" &> /dev/null; then
    echo -e "${GREEN}MongoDB connection successful!${NC}"
else
    echo -e "${RED}Failed to connect to MongoDB.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}MongoDB Setup Complete!${NC}"
echo "=============================="
echo "MongoDB is running on: mongodb://localhost:27017"
echo ""
echo "Next steps:"
echo "1. Install Python dependencies: pip install -r requirements.txt"
echo "2. Create .env file: cp .env.example .env"
echo "3. Seed the database: python utils/seed_database.py"
echo "4. Start the Flask app: python app.py"
echo ""
echo "To stop MongoDB later: brew services stop mongodb/brew/mongodb-community"
