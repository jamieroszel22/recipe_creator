# Recipe Creator - Docker Deployment

This guide explains how to deploy the Recipe Creator application using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start

1. Clone this repository:
   ```
   git clone https://github.com/jamieroszel22/recipe_creator.git
   cd recipe_creator
   ```

2. Build and start the containers:
   ```
   docker-compose up -d
   ```

3. Access the application:
   ```
   http://localhost:8000
   ```

## Sharing the Application

### Option 1: Share on the same network

If you want to share the application with others on the same network:

1. Find your machine's IP address:
   ```
   # On Windows
   ipconfig
   
   # On macOS/Linux
   ifconfig
   ```

2. Others can access the application at:
   ```
   http://<your-ip-address>:8000
   ```

### Option 2: Use a tunnel service

For sharing over the internet, you can use a tunnel service like ngrok:

1. Install ngrok from [ngrok.com](https://ngrok.com/)

2. Start a tunnel to your local application:
   ```
   ngrok http 8000
   ```

3. Share the provided ngrok URL with others

### Option 3: Deploy to a cloud provider

For a more permanent solution, deploy to a cloud provider:

1. Push your Docker image to a registry:
   ```
   docker build -t your-username/recipe-creator .
   docker push your-username/recipe-creator
   ```

2. Deploy to a service like DigitalOcean, AWS, or Azure using their container services

## Managing the Application

- View logs:
  ```
  docker-compose logs -f
  ```

- Stop the application:
  ```
  docker-compose down
  ```

- Restart the application:
  ```
  docker-compose restart
  ```

- Update the application:
  ```
  git pull
  docker-compose up -d --build
  ```

## Troubleshooting

- If the application doesn't start, check the logs:
  ```
  docker-compose logs -f
  ```

- If Ollama fails to download the model, you can manually pull it:
  ```
  docker exec -it recipe-creator-recipe-creator-1 ollama pull granite3.1-dense:8b
  ```

- If the application is slow, consider using a machine with more resources 

# Create a README.md file with project information
cat > README.md << 'EOF'
# Recipe Creator

A web application that creates recipes based on user-provided ingredients using the BeeAI framework and Flask.

## Features

- Enter ingredients you have on hand
- Get detailed recipes with ingredients and instructions
- Save favorite recipes
- Clean, user-friendly web interface
- Multi-agent AI system for better recipe generation

## Technologies Used

- Python with Flask for the web framework
- BeeAI framework for AI functionality
- Ollama with granite3.1-dense:8b model
- Docker for easy deployment and sharing

## Quick Start with Docker

1. Clone this repository:
   ```
   git clone https://github.com/jamieroszel22/recipe_creator.git
   cd recipe_creator
   ```

2. Build and start the containers:
   ```
   docker-compose up -d
   ```

3. Access the application:
   ```
   http://localhost:8000
   ```

For more detailed deployment instructions, see [README-DOCKER.md](README-DOCKER.md).

## Local Development Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run Ollama:
   ```
   ollama run granite3.1-dense:8b
   ```

4. Start the Flask app:
   ```
   python simple_app.py
   ```

5. Access the application:
   ```
   http://127.0.0.1:5000
   ```

## How It Works

This application uses a sequential multi-agent system:
1. The RecipeFinder agent searches for recipes using the provided ingredients
2. The Compiler agent formats and enhances the recipes
3. The Flask web application provides a user-friendly interface

## License

MIT License
EOF 