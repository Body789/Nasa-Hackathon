# app.py

import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env file
# This must be the first thing we do to load SECRET_KEY
load_dotenv()

# Initialize SQLAlchemy DB object globally
db = SQLAlchemy()

def create_app():
    # 1. Initialize the core application
    app = Flask(__name__, instance_relative_config=True)

    # 2. Configure the database (SQLite)
    # The database file will be stored in the instance folder (instance/app.db)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Set the secret key from the environment for session management
    # We use os.getenv() with a fallback for safety.
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a-very-weak-default-key-shhh')

    # 3. Initialize extensions
    db.init_app(app)

    # 4. Import models and ensure tables are created (Will be refined in the next step)
    with app.app_context():
        import models  # Import models.py to register table structure
        # db.create_all() will be called after defining the models for the first time
        
    # 5. A simple route to test the app is running
    @app.route('/')
    def index():
        # For now, a simple text response. Later, this will render a template.
        return "<h1>Kid-Friendly NASA App Backend Running!</h1><p>Ready for routes and data modeling.</p>"
    
    return app

# Main block for running the development server
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)