# Import SQLAlchemy - this is an ORM (Object-Relational Mapping) tool
# ORM lets us work with databases using Python objects instead of writing SQL queries
# Instead of "SELECT * FROM tasks", we can do Task.query.all()
from flask_sqlalchemy import SQLAlchemy

# Create a database object
# This will be used to interact with our database throughout the application
# We'll use this to add, query, update, and delete tasks
db = SQLAlchemy()

# Define the Task model
# A model is a Python class that represents a database table
# Each instance of Task represents one row in the tasks table
# When we create a Task object, it becomes a row in the database
class Task(db.Model):
    # Define the table name in the database
    # This is the actual name of the table in SQLite
    # The table will be called 'tasks'
    __tablename__ = 'tasks'
    
    # Define columns (fields) in the table
    # Each column stores one piece of information about a task
    
    # id column - primary key (unique identifier for each task)
    # Integer = number type
    # primary_key=True = this is the unique identifier (like a social security number for tasks)
    # Auto-increments: first task gets id=1, second gets id=2, etc.
    id = db.Column(db.Integer, primary_key=True)
    
    # title column - the task title/name
    # String(200) = text field, max 200 characters
    # nullable=False = this field is required (cannot be empty)
    # Every task must have a title
    title = db.Column(db.String(200), nullable=False)
    
    # status column - whether task is 'pending' or 'completed'
    # String(50) = text field, max 50 characters
    # default='pending' = if not specified when creating task, default to 'pending'
    # This satisfies requirement: Task Object must have 'status'
    status = db.Column(db.String(50), default='pending')
    
    # importance column - importance level from 1 to 5
    # Integer = number type
    # default=3 = if not specified when creating task, default to 3
    # This is for the extra feature (sorting by importance)
    importance = db.Column(db.Integer, default=3)
    
    # category column - task category (like 'work', 'personal', 'science')
    # String(100) = text field, max 100 characters
    # nullable=True = this field is optional (can be empty)
    # This is for the extra feature (filtering by category)
    category = db.Column(db.String(100), nullable=True)
    
    # due_date column - when the task is due
    # String(50) = text field (we'll store dates as strings like '2025-01-20')
    # nullable=True = this field is optional (can be empty)
    # This is for the extra feature (sorting by due date)
    due_date = db.Column(db.String(50), nullable=True)
    
    # This method converts a Task object to a dictionary
    # This is useful when we need to send task data as JSON to the frontend
    # The frontend expects a dictionary/object, not a Task model object
    def to_dict(self):
        # Return a dictionary with all task fields
        # This matches what the frontend expects: {id, title, status, importance, category, due_date}
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'importance': self.importance,
            'category': self.category,
            'due_date': self.due_date
        }

# Function to initialize the database
# This creates the database file and tables if they don't exist
# We call this once when the app starts
# Takes the Flask app as a parameter to avoid circular imports
def init_database(app):
    # Set the database URI (where to store the database file)
    # 'sqlite:///tasks.db' means create a file called 'tasks.db' in the current directory
    # SQLite stores everything in one file - easy to backup and move
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    
    # Disable tracking modifications (not needed, saves resources)
    # SQLAlchemy can track changes to objects, but we don't need that feature
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database with the Flask app
    # This connects SQLAlchemy to our Flask app
    # Now we can use 'db' to interact with the database
    db.init_app(app)
    
    # Create all tables defined by our models
    # This creates the 'tasks' table if it doesn't exist
    # If the table already exists, it does nothing (won't overwrite)
    # We use app.app_context() because Flask needs to know which app we're working with
    with app.app_context():
        db.create_all()
        
        # Create fake tasks if database is empty
        # This lets you see the frontend working immediately
        # Check if there are any tasks in the database
        if Task.query.count() == 0:
            # Create sample tasks with different categories and statuses
            # This helps test sorting, filtering, and displaying tasks
            
            # Task 1: Science task (pending)
            task1 = Task(
                title='Study for Chemistry Exam',
                status='pending',
                importance=5,
                category='science',
                due_date='2025-01-25'
            )
            
            # Task 2: Work task (completed)
            task2 = Task(
                title='Finish Project Report',
                status='completed',
                importance=4,
                category='work',
                due_date='2025-01-20'
            )
            
            # Task 3: Personal task (pending)
            task3 = Task(
                title='Buy Groceries',
                status='pending',
                importance=2,
                category='personal',
                due_date='2025-01-22'
            )
            
            # Task 4: Science task (pending)
            task4 = Task(
                title='Complete Lab Assignment',
                status='pending',
                importance=3,
                category='science',
                due_date='2025-01-23'
            )
            
            # Add all tasks to the database session
            db.session.add(task1)
            db.session.add(task2)
            db.session.add(task3)
            db.session.add(task4)
            
            # Commit the changes to save the tasks
            db.session.commit()