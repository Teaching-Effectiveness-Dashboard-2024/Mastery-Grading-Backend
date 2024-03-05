from flask import request, jsonify
from app import app, db
from app.models.models import User

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    api_token = data.get('api_token')  # Assuming you're directly receiving the API token for simplicity

    if not email or not password or not api_token:
        return jsonify({"msg": "Missing email, password, or API token"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 409

    user = User(email=email, password=password, api_token=api_token)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "Signup successful", "user": {"email": email, "api_token": api_token}}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        return jsonify({"msg": "Login successful", "api_token": user.api_token}), 200
    else:
        return jsonify({"msg": "Invalid email or password"}), 401
