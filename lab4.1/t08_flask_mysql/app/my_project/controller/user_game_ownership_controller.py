from flask import Blueprint, request, jsonify
from t08_flask_mysql.app.my_project.service.user_game_ownership_service import UserGameOwnershipService

user_game_bp = Blueprint('user_game_ownership', __name__)

@user_game_bp.route('/', methods=['GET'])
def get_all_ownerships():
    """
    Get all user-game ownerships
    ---
    tags:
      - UserGameOwnership
    responses:
      200:
        description: "List of all ownerships"
        schema:
          type: array
          items:
            type: object
            properties:
              OwnershipID:
                type: integer
              UserID:
                type: integer
              Username:
                type: string
              GameID:
                type: integer
              GameName:
                type: string
              PurchaseDate:
                type: string
    """
    ownerships = UserGameOwnershipService.get_all_ownerships()
    return jsonify([
        {
            "OwnershipID": o.OwnershipID,
            "UserID": o.UserID,
            "Username": o.user.Username,
            "GameID": o.GameID,
            "GameName": o.game.GameName,
            "PurchaseDate": o.PurchaseDate
        } for o in ownerships
    ])


@user_game_bp.route('/<int:ownership_id>', methods=['GET'])
def get_ownership_by_id(ownership_id):
    """
    Get a user-game ownership by ID
    ---
    tags:
      - UserGameOwnership
    parameters:
      - name: ownership_id
        in: path
        type: integer
        required: true
        description: "ID of the ownership"
    responses:
      200:
        description: "Ownership found"
        schema:
          type: object
          properties:
            OwnershipID:
              type: integer
            UserID:
              type: integer
            Username:
              type: string
            GameID:
              type: integer
            GameName:
              type: string
            PurchaseDate:
              type: string
      404:
        description: "Ownership not found"
    """
    ownership = UserGameOwnershipService.get_ownership_by_id(ownership_id)
    if ownership:
        return jsonify({
            "OwnershipID": ownership.OwnershipID,
            "UserID": ownership.UserID,
            "Username": ownership.user.Username,
            "GameID": ownership.GameID,
            "GameName": ownership.game.GameName,
            "PurchaseDate": ownership.PurchaseDate
        })
    return jsonify({"error": "Ownership not found"}), 404


@user_game_bp.route('/', methods=['POST'])
def create_ownership():
    """
    Create a new user-game ownership
    ---
    tags:
      - UserGameOwnership
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            UserID:
              type: integer
            GameID:
              type: integer
            PurchaseDate:
              type: string
    responses:
      201:
        description: "Ownership created"
        schema:
          type: object
          properties:
            OwnershipID:
              type: integer
            UserID:
              type: integer
            Username:
              type: string
            GameID:
              type: integer
            GameName:
              type: string
            PurchaseDate:
              type: string
    """
    data = request.get_json()
    ownership = UserGameOwnershipService.create_ownership(
        data['UserID'], data['GameID'], data.get('PurchaseDate')
    )
    return jsonify({
        "OwnershipID": ownership.OwnershipID,
        "UserID": ownership.UserID,
        "Username": ownership.user.Username,
        "GameID": ownership.GameID,
        "GameName": ownership.game.GameName,
        "PurchaseDate": ownership.PurchaseDate
    }), 201


@user_game_bp.route('/<int:ownership_id>', methods=['DELETE'])
def delete_ownership(ownership_id):
    """
    Delete a user-game ownership by ID
    ---
    tags:
      - UserGameOwnership
    parameters:
      - name: ownership_id
        in: path
        type: integer
        required: true
        description: "ID of the ownership"
    responses:
      204:
        description: "Ownership deleted"
      404:
        description: "Ownership not found"
    """
    success = UserGameOwnershipService.delete_ownership(ownership_id)
    if success:
        return jsonify({"message": "Ownership deleted"}), 204
    return jsonify({"error": "Ownership not found"}), 404


@user_game_bp.route('/link', methods=['POST'])
def link_user_to_game():
    """
    Link a user to a game
    ---
    tags:
      - UserGameOwnership
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            Username:
              type: string
            GameName:
              type: string
    responses:
      201:
        description: "User linked to game"
      400:
        description: "Bad request or error"
    """
    data = request.get_json()
    username = data.get('Username')
    game_name = data.get('GameName')

    if not username or not game_name:
        return jsonify({"error": "Username and GameName are required"}), 400

    try:
        UserGameOwnershipService.link_user_to_game(username, game_name)
        return jsonify({"message": f"User '{username}' linked to game '{game_name}'"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
