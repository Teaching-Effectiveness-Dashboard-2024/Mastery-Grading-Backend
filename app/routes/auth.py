from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from ..models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    api_token = data.get('api_token')

    if not email or not password or not api_token:
        return jsonify({"msg": "Missing email or password or api_token"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User with this email already exists"}), 409

    new_user = User(email=email, password=password, api_token=api_token)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to create user", "error": str(e)}), 500

    return jsonify({"msg": "User created successfully", "user": {"email": email}}), 201

@auth_bp.route('/login', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        return jsonify({"msg": "Login successful", "user": {"email": email, "api_token": user.api_token}}), 200
    else:
        return jsonify({"msg": "Login failed. Invalid email or password."}), 401
