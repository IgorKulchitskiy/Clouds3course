from flask import Blueprint, request, jsonify
from t08_flask_mysql.app.my_project.service.users_service import UsersService

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_all_users():
    """
    Get all users
    ---
    tags:
      - Users
    responses:
      200:
        description: "List of all users"
        schema:
          type: array
          items:
            type: object
            properties:
              UserID:
                type: integer
              Username:
                type: string
              Email:
                type: string
              PasswordHash:
                type: string
    """
    users = UsersService.get_all_users()
    return jsonify([{"UserID": u.UserID, "Username": u.Username, "Email": u.Email, "PasswordHash": u.PasswordHash} for u in users])

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Get a user by ID
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: "ID of the user"
    responses:
      200:
        description: "User found"
        schema:
          type: object
          properties:
            UserID:
              type: integer
            Username:
              type: string
            Email:
              type: string
      404:
        description: "User not found"
    """
    user = UsersService.get_user_by_id(user_id)
    if user:
        return jsonify({"UserID": user.UserID, "Username": user.Username, "Email": user.Email})
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            Username:
              type: string
            Email:
              type: string
            PasswordHash:
              type: string
    responses:
      201:
        description: "User created"
        schema:
          type: object
          properties:
            UserID:
              type: integer
            Username:
              type: string
            Email:
              type: string
    """
    data = request.get_json()
    user = UsersService.create_user(data['Username'], data['Email'], data['PasswordHash'])
    return jsonify({"UserID": user.UserID, "Username": user.Username, "Email": user.Email}), 201
