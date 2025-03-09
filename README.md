# Recipe Creator with BeeAI Framework

A web application that creates recipes based on user-provided ingredients using the BeeAI framework and Flask.

## Features

- Enter ingredients you have on hand
- Get detailed recipes with ingredients and instructions
- Clean, user-friendly web interface
- Real-time progress updates

## Prerequisites

Before running this application, make sure you have:

- Python 3.11 or higher
- [Ollama](https://ollama.ai/) installed with the granite3.1-dense:8b model
- A virtual environment (recommended)

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd recipe-creator
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Make sure Ollama is running with the required model:
   ```
   ollama run granite3.1-dense:8b
   ```

## Running the Application

1. Start the Flask web server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Enter your ingredients (separated by commas) and click "Generate Recipes"

4. Wait for the recipes to be generated (this may take several minutes)

## Usage

1. Enter ingredients you have available, separated by commas (e.g., "chicken, broccoli, rice, garlic")
2. Click "Generate Recipes" to start the process
3. Wait for the recipes to be generated (you'll see progress updates)
4. View the detailed recipes with ingredients and instructions
5. Click "Start New Search" to try with different ingredients

## How It Works

This application uses a multi-agent system built with the BeeAI framework:

1. The RecipeFinder agent searches for recipes using the provided ingredients
2. The Compiler agent formats the recipes in a clean, readable format
3. The Flask web application provides a user-friendly interface

## Troubleshooting

- If you encounter errors related to the LLM, make sure Ollama is running with the granite3.1-dense:8b model
- If the recipe generation takes too long, try using fewer ingredients
- If you get a "module not found" error, make sure all dependencies are installed

## License

This project is licensed under the MIT License - see the LICENSE file for details. 