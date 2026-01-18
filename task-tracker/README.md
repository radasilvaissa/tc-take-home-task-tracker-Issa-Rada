# READ ME: 

1. Images of the demo: 
    - Added to (task-tracker/images) -> there's two images, of the 
    main dashboard page, and of the page to add/edit/delete a task

2. Description of the project: 
    - A full-stack task management application built with React and Flask, that allows users to create, edit, and delete tasks. 
    - Includes sorting and searching capabilities, and consists of a React frontend with a Flask backend. 

3. Features: 
    - Create tasks with title, importance level, category, due date, and status
    - Edit, delete, create, and search tasks
    - Sort tasks by due date or importance level
    - Page design that works in mobile and desktop
        - For mobile it gets rid of sidebar, and since tasks are 
        organized in a grid, shows tasks that fit in the space

4. Pre-requisites to run with terminal: 
    - Have python 3.9 or higher installed
    - Node.js and npm installed 

5. How to run: 
    - Open two terminals 
    
    - Terminal 1: Backend
        - cd task-tracker
        - python3 -m venv venv
        (activate the virtual environment)
        - source venv/bin/activate
        - pip install flask flask-cors flask-sqlalchemy
        - cd backend
        - python3 app.py
        (the backend will run on localhost:5001)

    - Terminal 2: Frontend
        - cd task-tracker/frontend
        - npm install
        - npm start
        (the frontend will run on localhost:3000)