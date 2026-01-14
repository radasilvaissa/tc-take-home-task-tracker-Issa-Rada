# import Flask tools
# Blueprint = groups related routes together (keeps code organized)
# request = access data sent in HTTP request (like JSON body from frontend)
# jsonify = convert Python data to JSON response (frontend expects JSON)
from flask import Blueprint, request, jsonify

# import database and Task model
from database import db, Task

# allows us to keep roiutes in separaed files
# allows to add more routes later
api_bp = Blueprint('api', __name__)






# GET /api/tasks
# called when the Dashboard loads to fetch all tasks
@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    # task.query.all() gets all rows from the tasks table
    # returns a list of tasks
    tasks = Task.query.all()
    
    # convert each Task object to a dictionary
    # "For each task in tasks, call to_dict() and put result in a new list"
    tasks_list = [task.to_dict() for task in tasks]
    
    # return JSON list of tasks
    # jsonify converts the Python list to JSON format (what frontend expects)
    # 200 = HTTP status code for "OK" (success)
    return jsonify(tasks_list), 200







# GET /api/tasks/<id> - Get one task by ID
# called when EditTask page loads to get the task being edited
@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # find the task with the given ID, or none if not found
    task = Task.query.get(task_id)
    
    # if task doesn't exist, return 404 error
    # 404 = HTTP status code for "Not Found"
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # return the task as JSON
    # 200 = HTTP status code for "OK" (success)
    return jsonify(task.to_dict()), 200








# POST /api/tasks - Create a new task
# called when user submits the Create Task form
@api_bp.route('/tasks', methods=['POST'])
def create_task():
    # request.get_json() parses the JSON and returns a Python dictionary
    data = request.get_json()
    
    # extract fields from the data
    # if a field is not provided, use the default value
    title = data.get('title')
    status = data.get('status', 'pending')
    importance = data.get('importance', 3)
    category = data.get('category', '')
    due_date = data.get('due_date', '')
    
    # if title is missing or empty, return an error
    # 400 = HTTP status code for "Bad Request" (client sent invalid data)
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    # create a new Task object
    # pass all the fields we extracted from the request
    new_task = Task(
        title=title,
        status=status,
        importance=importance,
        category=category,
        due_date=due_date
    )
    
    # add the new task to the database session
    # stages the commit
    db.session.add(new_task)
    
    # commit the changes to the database
    db.session.commit()
    
    # return the created task as JSON
    # 201 = HTTP status code for "Created" (successful creation)
    return jsonify(new_task.to_dict()), 201








# PUT /api/tasks/<id> - Update an existing task
# called when user submits the Edit Task form
@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # find the task with the given ID
    task = Task.query.get(task_id)
    
    # if task doesn't exist, return 404 error
    # 404 = HTTP status code for "Not Found"
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # get JSON data from the request body
    data = request.get_json()
    
    # update task fields with new values
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
    
    # commit the changes to the database
    db.session.commit()
    
    # return the updated task as JSON
    # 200 = HTTP status code for "OK" (successful update)
    return jsonify(task.to_dict()), 200








# DELETE /api/tasks/<id> - Delete a task
# This is called when user clicks the Delete button
@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # find the task with the given ID
    task = Task.query.get(task_id)
    
    # if task doesn't exist, return 404 error
    # 404 = HTTP status code for "Not Found"
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # delete the task from the database
    db.session.delete(task)
    
    # commit the changes to the database
    db.session.commit()
    
    # return success message
    # 200 = HTTP status code for "OK" (successful deletion)
    return jsonify({'message': 'Task deleted successfully'}), 200