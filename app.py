from flask import Flask, render_template, request, jsonify
import asyncio
import threading
import time
from recipe_creator import generate_recipes

app = Flask(__name__)

# Store ongoing tasks
tasks = {}

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
        'start_time': time.time()
    }
    
    # Start the recipe generation in a background thread
    def run_recipe_task():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Run the recipe generation
            result = loop.run_until_complete(generate_recipes(ingredients))
            
            # Update task with result
            tasks[task_id]['status'] = 'completed'
            tasks[task_id]['result'] = result
            tasks[task_id]['progress'] = 100
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
        # Estimate progress (max 95% until complete)
        estimated_progress = min(95, int(elapsed_time / 60 * 10))  # ~10% per minute
        task['progress'] = estimated_progress
    
    return jsonify({
        'status': task['status'],
        'progress': task['progress'],
        'result': task['result']
    })

@app.route('/clear/<task_id>', methods=['POST'])
def clear_task(task_id):
    """Clear a completed task from memory"""
    if task_id in tasks:
        del tasks[task_id]
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True) 