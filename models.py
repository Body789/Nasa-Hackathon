# models.py

from app import db  # Use relative import to get the shared db object
from datetime import datetime
from sqlalchemy.orm import relationship # Optional, but clarifies relationships

# --- 1. User Model (Table: users) ---
# Used for FR6 (Login) and FR7 (Admin)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    # is_admin flag for FR7 (Admin approval)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships (Allows us to access linked data easily)
    challenges = relationship('Challenge', backref='creator', lazy=True)
    solutions = relationship('Solution', backref='author', lazy=True)

    def __repr__(self):
        return f"<User {self.nickname}>"

# --- 2. Challenge Model (Table: challenges) ---
# Used for FR1 (List challenges) and FR2 (Add challenge)
class Challenge(db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Default is False, must be approved by an Admin (FR7)
    approved = db.Column(db.Boolean, default=False)  
    
    # Foreign Key: Links the challenge back to the User who created it
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship: Allows Challenge.solutions to return all associated solutions
    solutions = relationship('Solution', backref='challenge', lazy=True)

    def __repr__(self):
        return f"<Challenge {self.title}>"

# --- 3. Solution Model (Table: solutions) ---
# Used for FR3 (Submit solution) and FR4 (Display gallery)
class Solution(db.Model):
    __tablename__ = 'solutions'
    id = db.Column(db.Integer, primary_key=True)
    # Submission content can be text, a link, or an image path
    content = db.Column(db.Text, nullable=True)     
    link = db.Column(db.String(500), nullable=True) # For sandbox links
    image_path = db.Column(db.String(300), nullable=True) # Path to uploaded image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Default is False, must be approved by an Admin (FR7)
    approved = db.Column(db.Boolean, default=False) 

    # Foreign Key: Links the solution to a specific Challenge
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    # Foreign Key: Links the solution back to the User who submitted it
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f"<Solution for Challenge ID {self.challenge_id} by User ID {self.created_by}>"

# --- 4. Planet Model (Table: planets) ---
# Used for FR8 (Interactive Solar System Data)
class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    fun_fact = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Planet {self.name}>"