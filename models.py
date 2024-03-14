from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Storing passwords in plaintext
    api_token = db.Column(db.String(255), unique=True, nullable=False)
    canvasUserId = db.Column(db.Integer, unique=True, nullable=False)