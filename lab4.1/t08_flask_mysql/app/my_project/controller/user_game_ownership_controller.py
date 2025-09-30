from flask import Blueprint, request, jsonify
from t08_flask_mysql.app.my_project.service.user_game_ownership_service import UserGameOwnershipService

user_game_bp = Blueprint('user_game_ownership', __name__)

@user_game_bp.route('/', methods=['GET'])
def get_all_ownerships():
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
    success = UserGameOwnershipService.delete_ownership(ownership_id)
    if success:
        return jsonify({"message": "Ownership deleted"}), 204
    return jsonify({"error": "Ownership not found"}), 404

@user_game_bp.route('/link', methods=['POST'])
def link_user_to_game():
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
