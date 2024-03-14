from flask import Blueprint, request, jsonify
from models import User, db
from flask_cors import CORS, cross_origin
login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def login():
    # Your login route code here
    print("entered login")
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400
    
    user = User.query.filter_by(email=email).first()
    print(user)
    if user and user.password == password:
        # Cache the API token with the user's email as the key
        # cache.set(email, user.api_token, timeout=60 * 60)  # Cache timeout of 60 minutes
        #print("cached token successfully")

        print("logged in successfully")

        return jsonify({"msg": "Login successful", "user": {"email": email}}), 200
    else:
        return jsonify({"msg": "Login failed. Invalid email or password."}), 401

@login_bp.route('/signup', methods=['POST'])
def signup():
    # Your signup route code here
    print("entered signup")
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    api_token = data.get('api_token')

    if not email or not password or not api_token:
        return jsonify({"msg": "Missing email or password or api_token"}), 400

    print(email)
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User with this email already exists"}), 409

    new_user = User(email=email, password=password, api_token=api_token)  # Directly storing the hashed password
    print("created dummy user")
    try:
        db.session.add(new_user)
        print("added to db")
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("in exception")
        return jsonify({"msg": "Failed to create user", "error": str(e)}), 500
    print("signed successfully")

    return jsonify({"msg": "User created successfully", "user": {"email": email}}), 201
