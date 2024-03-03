from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# Sample user data for demonstration purposes
# In a real application, you would check against data in your database
users = {
    "user1": "email",
    "user2": "password"
}


@app.route('/login', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def login():
    # Ensure that the request contains JSON data
    print("entered login")
    # print(request.is_json)
    # if not request.is_json:
    #     return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    print(data)
    username = data.get('email')
    password = data.get('password')
    print(username + " " + password)
    # # Basic validation
    # if not username or not password:
    #     return jsonify({"msg": "Missing username or password"}), 400
    #
    # # Check if the user exists and the password matches
    # # (For demonstration, using a simple dictionary. Replace with your database logic.)
    # if username in users and users[username] == password:
    #     return jsonify({"msg": "Login successful", "user": username}), 200
    # else:
    #     return jsonify({"msg": "Login failed"}), 401
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True)
