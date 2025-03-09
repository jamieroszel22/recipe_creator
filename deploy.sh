#!/bin/bash

# Make script exit on any error
set -e

echo "Recipe Creator - Deployment Script"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Build and start the containers
echo "Building and starting containers..."
docker-compose up -d --build

# Wait for the application to start
echo "Waiting for the application to start..."
sleep 10

# Check if the application is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "Application is running!"
    echo "You can access it at: http://localhost:8000"
    
    # Get the IP address for sharing on the same network
    if command -v ipconfig &> /dev/null; then
        # Windows
        IP=$(ipconfig | grep -i "IPv4 Address" | head -n 1 | awk '{print $NF}')
    else
        # Linux/macOS
        IP=$(hostname -I | awk '{print $1}')
    fi
    
    if [ ! -z "$IP" ]; then
        echo "Share on your network at: http://$IP:8000"
    fi
    
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
else
    echo "Application failed to start. Check logs with: docker-compose logs -f"
fi 