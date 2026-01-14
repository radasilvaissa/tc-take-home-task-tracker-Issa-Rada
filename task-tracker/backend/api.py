# Import Flask tools
# Blueprint = groups related routes together (keeps code organized)
# request = access data sent in HTTP request (like JSON body from frontend)
# jsonify = convert Python data to JSON response (frontend expects JSON)
from flask import Blueprint, request, jsonify

# Import database and Task model
# We need these to interact with the database
# db = database object for queries
# Task = the model class representing tasks in the database
from database import db, Task

# Create a Blueprint for our API routes
# Blueprint groups related routes together
# 'api_bp' is the name, __name__ tells Flask where to find it
# We'll register this blueprint in app.py with prefix '/api'
api_bp = Blueprint('api', __name__)

# GET /api/tasks - Get all tasks
# This is called when the Dashboard loads to fetch all tasks
# Requirement: "Create GET /api/tasks endpoint"
# The frontend calls: GET http://localhost:5000/api/tasks
@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    # Query all tasks from the database
    # Task.query.all() gets all rows from the tasks table
    # This returns a list of Task objects
    tasks = Task.query.all()
    
    # Convert each Task object to a dictionary
    # The frontend expects a list of task objects (dictionaries)
    # to_dict() converts our Task model to a dictionary
    # List comprehension: [task.to_dict() for task in tasks] means:
    # "For each task in tasks, call to_dict() and put result in a new list"
    tasks_list = [task.to_dict() for task in tasks]
    
    # Return JSON response
    # jsonify converts the Python list to JSON format (what frontend expects)
    # 200 = HTTP status code for "OK" (success)
    # This satisfies requirement: "Return JSON list of tasks"
    return jsonify(tasks_list), 200

# GET /api/tasks/<id> - Get one task by ID
# This is called when EditTask page loads to get the task being edited
# The frontend calls: GET http://localhost:5000/api/tasks/1 (where 1 is the task ID)
# <int:task_id> means Flask will extract the ID from the URL and convert it to an integer
@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Find the task with the given ID
    # Task.query.get(task_id) looks up a task by its primary key (id)
    # This returns a Task object if found, or None if not found
    task = Task.query.get(task_id)
    
    # If task doesn't exist, return 404 error
    # 404 = HTTP status code for "Not Found"
    # We return an error message so the frontend knows what went wrong
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Return the task as JSON
    # to_dict() converts Task object to dictionary, jsonify converts to JSON
    # 200 = HTTP status code for "OK" (success)
    return jsonify(task.to_dict()), 200

# POST /api/tasks - Create a new task
# This is called when user submits the Create Task form
# The frontend calls: POST http://localhost:5000/api/tasks with JSON body
# POST is used for creating new resources
@api_bp.route('/tasks', methods=['POST'])
def create_task():
    # Get JSON data from the request body
    # The frontend sends task data as JSON in the request body
    # request.get_json() parses the JSON and returns a Python dictionary
    # Example: {'title': 'Buy groceries', 'status': 'pending', 'importance': 3}
    data = request.get_json()
    
    # Extract fields from the data
    # The frontend sends: title, importance, category, due_date, status
    # .get() method gets a value from dictionary, with optional default value
    # If a field is not provided, use the default value
    title = data.get('title')
    status = data.get('status', 'pending')  # Default to 'pending' if not provided
    importance = data.get('importance', 3)  # Default to 3 if not provided
    category = data.get('category', '')  # Default to empty string if not provided
    due_date = data.get('due_date', '')  # Default to empty string if not provided
    
    # Validate that title is provided (it's required)
    # If title is missing or empty, return an error
    # 400 = HTTP status code for "Bad Request" (client sent invalid data)
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    # Create a new Task object
    # This creates a new row that will be inserted into the database
    # We pass all the fields we extracted from the request
    new_task = Task(
        title=title,
        status=status,
        importance=importance,
        category=category,
        due_date=due_date
    )
    
    # Add the new task to the database session
    # This stages it for insertion (doesn't actually save yet)
    # Think of it like adding an item to a shopping cart - not checked out yet
    db.session.add(new_task)
    
    # Commit the changes to the database
    # This actually saves the task to the database file
    # Think of it like checking out - now the item is actually purchased
    # If we don't commit, the task won't be saved
    db.session.commit()
    
    # Return the created task as JSON
    # The frontend can use this to confirm the task was created
    # 201 = HTTP status code for "Created" (successful creation)
    return jsonify(new_task.to_dict()), 201

# PUT /api/tasks/<id> - Update an existing task
# This is called when user submits the Edit Task form
# The frontend calls: PUT http://localhost:5000/api/tasks/1 with JSON body
# PUT is used for updating existing resources
# <int:task_id> extracts the task ID from the URL
@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # Find the task with the given ID
    # Task.query.get(task_id) looks up a task by its primary key (id)
    task = Task.query.get(task_id)
    
    # If task doesn't exist, return 404 error
    # 404 = HTTP status code for "Not Found"
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Get JSON data from the request body
    # The frontend sends updated task data
    # Example: {'title': 'Updated title', 'status': 'completed'}
    data = request.get_json()
    
    # Update task fields with new values
    # Only update fields that are provided in the request
    # .get() with second parameter keeps existing value if not provided
    # We check 'if field in data' to only update fields that were sent
    if 'title' in data:
        task.title = data.get('title')
    if 'status' in data:
        task.status = data.get('status')
    if 'importance' in data:
        task.importance = data.get('importance')
    if 'category' in data:
        task.category = data.get('category')
    if 'due_date' in data:
        task.due_date = data.get('due_date')
    
    # Commit the changes to the database
    # This saves the updated task to the database file
    # Without commit, changes won't be saved
    db.session.commit()
    
    # Return the updated task as JSON
    # The frontend can use this to confirm the task was updated
    # 200 = HTTP status code for "OK" (successful update)
    return jsonify(task.to_dict()), 200

# DELETE /api/tasks/<id> - Delete a task
# This is called when user clicks the Delete button
# The frontend calls: DELETE http://localhost:5000/api/tasks/1
# DELETE is used for removing resources
# <int:task_id> extracts the task ID from the URL
@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Find the task with the given ID
    # Task.query.get(task_id) looks up a task by its primary key (id)
    task = Task.query.get(task_id)
    
    # If task doesn't exist, return 404 error
    # 404 = HTTP status code for "Not Found"
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Delete the task from the database
    # This removes the row from the tasks table
    # db.session.delete(task) marks the task for deletion
    db.session.delete(task)
    
    # Commit the changes to the database
    # This actually removes the task from the database file
    # Without commit, the task won't be deleted
    db.session.commit()
    
    # Return success message
    # The frontend can use this to confirm the task was deleted
    # 200 = HTTP status code for "OK" (successful deletion)
    return jsonify({'message': 'Task deleted successfully'}), 200