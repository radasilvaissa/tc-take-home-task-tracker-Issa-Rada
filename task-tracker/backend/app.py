from flask import Flask

# import CORS to allows frontend to talk to our backend
# without CORS, browsers block requests between different ports/origins for security
from flask_cors import CORS

# import database setup function, create if not exist
# self-made function in database.py
from database import init_database

# import our API routes with all endpoints
# self-made function in api.py
from api import api_bp

# create the Flask application
app = Flask(__name__)

# enable CORS for all routes
CORS(app)

# initialize the database
# creates the database file (tasks.db) and tables if they don't exist
# Pass the app to init_database to avoid circular imports
init_database(app)

# connects all our routes (from api.py) to the Flask app
# "/api" prefix means all routes will start with /api
app.register_blueprint(api_bp, url_prefix='/api')

# runs the Flask server
# __name__ == '__main__' means this file is being run directly
# debug=True shows detailed error messages in browser
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)