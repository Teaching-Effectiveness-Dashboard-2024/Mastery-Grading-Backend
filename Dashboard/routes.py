from flask import Blueprint, request, jsonify
from models import User
from flask_cors import CORS, cross_origin
from utils import GetCanvasUser
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def dashboard():
    print("entered dashboard")
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"msg": "Invalid request: Missing email"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.api_token and user.canvasUserId:
        try:
            canvas = GetCanvasUser(user.api_token)
            canvasUser = canvas.get_user(user.canvasUserId)
            avatars = canvasUser.get_avatars()
            avatar_url = avatars[0].url if avatars else None
            name = str(canvasUser).split('(')[0]
            return jsonify({
                "msg": "Data fetched successfully",
                "user": {"email": email, "name": name, "imageURL": avatar_url}
            }), 200
        except Exception as e:
            print("Error fetching data:", e)
            return jsonify({"msg": "Error fetching data"}), 500
    else:
        return jsonify({"msg": "Data failed to load"}), 401
