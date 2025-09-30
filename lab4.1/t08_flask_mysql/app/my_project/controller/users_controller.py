from flask import Blueprint, request, jsonify
from t08_flask_mysql.app.my_project.service.users_service import UsersService

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_all_users():
    users = UsersService.get_all_users()
    return jsonify([{"UserID": u.UserID, "Username": u.Username, "Email": u.Email, "PasswordHash": u.PasswordHash} for u in users])

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = UsersService.get_user_by_id(user_id)
    if user:
        return jsonify({"UserID": user.UserID, "Username": user.Username, "Email": user.Email})
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UsersService.create_user(data['Username'], data['Email'], data['PasswordHash'])
    return jsonify({"UserID": user.UserID, "Username": user.Username, "Email": user.Email}), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = UsersService.update_user(user_id, data['Username'], data['Email'], data['PasswordHash'])
    if user:
        return jsonify({"UserID": user.UserID, "Username": user.Username, "Email": user.Email})
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = UsersService.delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted"}), 204
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/procedure', methods=['POST'])
def create_user_via_procedure():
    data = request.get_json()
    UsersService.create_user_via_procedure(data['Username'], data['Email'], data['PasswordHash'])
    return jsonify({"message": "User created via stored procedure"}), 201
