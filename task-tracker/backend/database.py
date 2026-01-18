# use SQLite database, a file-based db that stores data in a file on a disk (task.db)
# SQLAlchemy lets is work witn dbs using python objects instead of SQL queries
from flask_sqlalchemy import SQLAlchemy

# create a database object
# use this to query tasks
db = SQLAlchemy()

# Python class that represents a database table
# each instance of Task represents one row in the tasks table
class Task(db.Model):
    # The table will be called 'tasks'
    __tablename__ = 'tasks'
    
    # Define columns (fields) in the table
    
    # id column - primary key (unique identifier for each task)
    # auto-increments: first task gets id=1, second gets id=2, etc.
    id = db.Column(db.Integer, primary_key=True)
    
    # title column - the task title/name
    # this field is required (cannot be empty)
    title = db.Column(db.String(200), nullable=False)
    
    # status column - whether task is 'pending' or 'completed'
    # default='pending' = if not specified when creating task, default to 'pending'
    status = db.Column(db.String(50), default='pending')
    
    # importance column - importance level from 1 to 5
    # default=1 = if not specified when creating task, default to 1
    importance = db.Column(db.Integer, default=1)
    
    # category column - task category
    # nullable=True = this field is optional (can be empty)
    category = db.Column(db.String(100), nullable=True)
    
    # due_date column - when the task is due
    # String(50) = text field (we'll store dates as strings like '2025-01-20')
    due_date = db.Column(db.String(50), nullable=True)
    
    # converts a Task object to a dictionary
    # useful when we need to send task data as JSON to the frontend
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'importance': self.importance,
            'category': self.category,
            'due_date': self.due_date
        }

# function to initialize the database
# called when we initialize app
def init_database(app):
    # database URI (where to store the database file)
    # 'sqlite:///tasks.db' means create a file called 'tasks.db' in the current directory
    # SQLite stores everything in one file - easy to backup and move
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    
    # initialize the database with the Flask app
    # use 'db' to interact with the database
    db.init_app(app)
    
    # create all tables defined by our models
    with app.app_context():
        db.create_all()
        
        # Create fake tasks if database is empty
        # This lets you see the frontend working immediately
        if Task.query.count() == 0:
            
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