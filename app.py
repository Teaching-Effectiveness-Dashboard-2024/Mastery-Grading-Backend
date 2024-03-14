from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from canvasapi import Canvas
from datetime import datetime

from flask_caching import Cache

app = Flask(__name__)
CORS(app)

# Database configuration
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:rootgrading@database-mastery-grading.cx0k4s4omp9i.us-east-1.rds.amazonaws.com:5432/mastery_database"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure cache to use Redis
# app.config['CACHE_TYPE'] = 'RedisCache'
# app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'  # Assumes Redis is running on localhost, default port

# cache = Cache(app)

db = SQLAlchemy(app)


# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Storing passwords in plaintext
    api_token = db.Column(db.String(255), unique=True, nullable=False)
    canvasUserId = db.Column(db.Integer, unique=True, nullable=False)



class Mapping(db.Model):

    mappingId = db.Column(db.Integer, primary_key=True)
    mappingName = db.Column(db.String(120), unique=True, nullable=False)
    canvasUserId = db.Column(db.Integer, nullable=False)
    classId = db.Column(db.Integer, unique=True, nullable=False)
    className = db.Column(db.String(120), unique=True, nullable=False)
    mapping = db.Column(db.JSON, nullable=False)  # Added JSON column, nullable is set to True by default
    createdAt = db.Column(db.DateTime, default=datetime.now())  # Assuming you want UTC time
    updatedAt = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


# Create the database tables based on the models
with app.app_context():
    db.create_all()



@app.route('/signup', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def signup():
    # print("entered signup")
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    api_token = data.get('api_token')

    if not email or not password or not api_token:
        return jsonify({"msg": "Missing email or password or api_token"}), 400

    # print(email)
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User with this email already exists"}), 409

    new_user = User(email=email, password=password, api_token=api_token)  # Directly storing the hashed password
    # print("created dummy user")
    try:
        db.session.add(new_user)
        # print("added to db")
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # print("in exception")
        return jsonify({"msg": "Failed to create user", "error": str(e)}), 500
    print("signed successfully")

    return jsonify({"msg": "User created successfully", "user": {"email": email}}), 201


@app.route('/login', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def login():
    # print("entered login")
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        # Cache the API token with the user's email as the key
        # cache.set(email, user.api_token, timeout=60 * 60)  # Cache timeout of 60 minutes
        # print("cached token successfully")

        print("logged in successfully")

        return jsonify({"msg": "Login successful", "user": {"email": email}}), 200
    else:
        return jsonify({"msg": "Login failed. Invalid email or password."}), 401


def GetCanvasUser(api_token):
    API_URL = "https://sjsu.instructure.com/"
    return Canvas(API_URL, api_token)


@app.route('/dashboard', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def dashboard():
    # print("entered dashboard")
    data = request.get_json()
    email = data.get('email')
    # print(email)

    if not email:
        return jsonify({"msg": "Invalid request: Missing email "}), 400

    user = User.query.filter_by(email=email).first()
    print(user)
    if user and user.api_token and user.canvasUserId:

        print("Data fetched successfully")
        canvas = GetCanvasUser(user.api_token)
        canvasUser = canvas.get_user(user.canvasUserId)

        # print("user is:" + str(canvasUser))
        avatars = canvasUser.get_avatars()
        for avatar in avatars:
            print(avatar.url)
        name = str(canvasUser)
        name = name.split('(')[0]
        print("exiting Dashboard with" + name)

        return jsonify({"msg": "Data fetched successfully",
                        "user": {"email": email, "name": name, "imageURL": str(avatars[1].url)}}), 200
    else:
        return jsonify({"msg": "Data failed to load"}), 401


@app.route('/mapping', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def mapping():
    print("entered mapping")
    data = request.get_json()
    email = data.get('email')
    print(email)

    if not email:
        return jsonify({"msg": "Invalid request: Missing email "}), 400

    user = User.query.filter_by(email=email).first()
    print(user)
    if user and user.api_token and user.canvasUserId:
        print("Data fetched successfully")
        canvas = GetCanvasUser(user.api_token)
        canvasUser = canvas.get_user(user.canvasUserId)

        # print("user is:" + str(canvasUser))

        name = str(canvasUser)
        name = name.split('(')[0]
        name = name[:len(name) - 1]
        print(name)

        courses = canvasUser.get_courses(enrollment_state="active", enrollment_type="teacher")
        # print(courses)
        # print("courses are" + courses)
        for course in courses:
            print(course)

        # for course id = course.id

        # print("course is" + course)

        return jsonify({"msg": "Data fetched successfully", "user": {"email": email, }}), 200
    else:
        return jsonify({"msg": "Data failed to load"}), 401


@app.route('/mappingTable', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def mappingTable():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"msg": "Invalid request: Missing email "}), 400

    user = User.query.filter_by(email=email).first()


    if user:
        mappings = Mapping.query.filter_by(canvasUserId=user.canvasUserId).all()
        if mappings:
            # Serialize the mappings
            mappings_list = [{"mappingId": mapping.mappingId,
                              "mappingName": mapping.mappingName,
                              "canvasUserId": mapping.canvasUserId,
                              "classId": mapping.classId,
                              "className": mapping.className,
                              "mapping": mapping.mapping,
                              "createdAt": mapping.createdAt,
                              "updatedAt": mapping.updatedAt} for mapping in mappings]

            return jsonify({"msg": "Data fetched successfully", "mappings": mappings_list}), 200
        else:
            return jsonify({"msg": "No Mappings for the user"}), 200
    else:
        return jsonify({"msg": "Failed to fetch all user details"}), 401


if __name__ == '__main__':
    app.run(debug=True)
