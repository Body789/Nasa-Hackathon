# app.py

import os
import click # Required for the init-db command
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime # Required for seeding logic

# Load environment variables from .env file
load_dotenv()

# Initialize SQLAlchemy DB object globally
db = SQLAlchemy()

# You must import models here, after 'db' is created, so the seed function can use them
from models import User, Challenge, Solution, Planet # Importing all models now

# --- FUNCTION: Define the Seeding Logic ---
def seed_planet_data():
    """Inserts static planet data into the Planet table."""
    
    planets_data = [
        {"name": "Sun", "description": "The star at the center of our solar system. Essential for life on Earth.", "fun_fact": "The Sun makes up 99.8% of the total mass of the solar system!"},
        {"name": "Mercury", "description": "The smallest planet, closest to the Sun.", "fun_fact": "A year on Mercury is only 88 Earth days long!"},
        {"name": "Venus", "description": "The hottest planet, covered in thick, toxic clouds.", "fun_fact": "Venus spins backward compared to most other planets."},
        {"name": "Earth", "description": "Our home planet, the only one known to harbor life.", "fun_fact": "Earth's rotation is slowing down, meaning days are getting longer."},
        {"name": "Mars", "description": "The 'Red Planet,' a cold, dusty world with a thin atmosphere.", "fun_fact": "Mars has the tallest mountain and largest volcano in the solar system, Olympus Mons."},
        {"name": "Jupiter", "description": "The largest planet, a gas giant known for its Great Red Spot.", "fun_fact": "Jupiter is so large, all the other planets could fit inside it."},
        {"name": "Saturn", "description": "A gas giant famous for its spectacular system of rings.", "fun_fact": "Saturn is the least dense planet—it would float in a giant bathtub!"},
        {"name": "Uranus", "description": "An ice giant that appears blue-green due to methane gas.", "fun_fact": "Uranus rotates on its side, making it look like a rolling ball."},
        {"name": "Neptune", "description": "The farthest known planet, cold and dark with supersonic winds.", "fun_fact": "Neptune takes nearly 165 Earth years to orbit the Sun."},
    ]
    
    if Planet.query.count() == 0:
        for data in planets_data:
            planet = Planet(name=data['name'], description=data['description'], fun_fact=data['fun_fact'])
            db.session.add(planet)
        
        db.session.commit()
        print(f"Seeded {len(planets_data)} celestial bodies.")
    else:
        print("Planet data already exists. Skipping seeding.")

# --- FUNCTION: Define the CLI command (init-db) ---
@click.command('init-db')
def init_db_command():
    """Clear existing data and create new tables, then seed static data."""
    # We must call create_app() to get an app context for the CLI command
    with create_app().app_context():
        # Drops ALL existing tables for a clean start in development
        db.drop_all() 
        db.create_all() # Recreates all tables based on models.py
        seed_planet_data()
        
        # Create an initial Admin user for FR7 testing (nickname: Admin)
        if User.query.filter_by(nickname='Admin').first() is None:
            admin_user = User(nickname='Admin', is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
            click.echo('Created default Admin user.')

        click.echo('Initialized and Seeded the database successfully.')


def create_app():
    # 1. Initialize the core application
    app = Flask(__name__, instance_relative_config=True)

    # 2. Configure the database (SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a-very-weak-default-key-shhh')

    # 3. Initialize extensions
    db.init_app(app)

    # 4. Register Command to initialize database (for seeding)
    with app.app_context():
        # import models is no longer necessary inside this block since we imported 
        # all models above the create_app function.
        app.cli.add_command(init_db_command)

    # 5. A simple route to test the app is running
    @app.route('/')
    def index():
        # For now, a simple text response.
        return "<h1>Kid-Friendly NASA App Backend Running!</h1><p>Ready for routes and data modeling.</p>"
    
    return app

# Main block for running the development server
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)