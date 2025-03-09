from flask import Flask, render_template, request, jsonify
import asyncio
import threading
import time
import datetime
import requests
from simple_recipe_creator import generate_simple_recipe

app = Flask(__name__)

# Store ongoing tasks
tasks = {}

def check_ollama_status():
    """Check if Ollama is running and the model is available"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            granite_models = [m for m in models if "granite" in m.get("name", "")]
            if granite_models:
                return {"status": "available", "models": [m["name"] for m in granite_models]}
            else:
                return {"status": "no_granite_models"}
        return {"status": "ollama_running_but_error"}
    except Exception as e:
        return {"status": "unavailable", "error": str(e)}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle recipe generation request"""
    ingredients = request.form.get('ingredients', '')
    
    if not ingredients:
        return jsonify({'error': 'No ingredients provided'}), 400
    
    # Generate a task ID
    task_id = str(int(time.time()))
    
    # Store task info
    tasks[task_id] = {
        'status': 'processing',
        'progress': 0,
        'result': None,
        'start_time': time.time(),
        'current_agent': 'RecipeFinder'
    }
    
    # Start the recipe generation in a background thread
    def run_recipe_task():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Run the recipe generation
            result = loop.run_until_complete(generate_simple_recipe(ingredients))
            
            # Update task with result
            tasks[task_id]['status'] = 'completed'
            tasks[task_id]['result'] = result
            tasks[task_id]['progress'] = 100
            tasks[task_id]['current_agent'] = None
        except Exception as e:
            tasks[task_id]['status'] = 'error'
            tasks[task_id]['result'] = f"Error: {str(e)}"
        finally:
            loop.close()
    
    # Start the background thread
    thread = threading.Thread(target=run_recipe_task)
    thread.daemon = True
    thread.start()
    
    return jsonify({'task_id': task_id})

@app.route('/status/<task_id>')
def status(task_id):
    """Check the status of a recipe generation task"""
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = tasks[task_id]
    
    # Calculate elapsed time for progress estimation
    if task['status'] == 'processing':
        elapsed_time = time.time() - task['start_time']
        
        # Estimate progress based on elapsed time
        if elapsed_time < 300:  # First 5 minutes: RecipeFinder
            estimated_progress = min(45, int(elapsed_time / 300 * 45))  # Max 45%
            task['current_agent'] = 'RecipeFinder'
        elif elapsed_time < 480:  # Next 3 minutes: Compiler
            estimated_progress = min(90, 45 + int((elapsed_time - 300) / 180 * 45))  # Max 90%
            task['current_agent'] = 'Compiler'
        else:
            estimated_progress = 95  # Final compilation
        
        task['progress'] = estimated_progress
    
    return jsonify({
        'status': task['status'],
        'progress': task['progress'],
        'result': task['result'],
        'current_agent': task.get('current_agent')
    })

@app.route('/clear/<task_id>', methods=['POST'])
def clear_task(task_id):
    """Clear a completed task from memory"""
    if task_id in tasks:
        del tasks[task_id]
    return jsonify({'success': True})

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'ollama': check_ollama_status(),
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting Recipe Creator Flask App with Sequential Multi-Agent System...")
    print("Make sure Ollama is running with: ollama run granite3.1-dense:8b")
    app.run(debug=True)