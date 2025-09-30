from flask import Blueprint, request, jsonify
from t08_flask_mysql.app.my_project.service.games_service import GamesService

games_bp = Blueprint('games', __name__)

@games_bp.route('/', methods=['GET'])
def get_all_games():
    games = GamesService.get_all_games()
    return jsonify([{"GameID": g.GameID, "GameName": g.GameName, "PublisherID": g.PublisherID, "ReleaseDate": g.ReleaseDate} for g in games])

@games_bp.route('/<int:game_id>', methods=['GET'])
def get_game_by_id(game_id):
    game = GamesService.get_game_by_id(game_id)
    if game:
        return jsonify({"GameID": game.GameID, "GameName": game.GameName, "PublisherID": game.PublisherID, "ReleaseDate": game.ReleaseDate})
    return jsonify({"error": "Game not found"}), 404

@games_bp.route('/', methods=['POST'])
def create_game():
    data = request.get_json()
    game = GamesService.create_game(data['GameName'], data['PublisherID'], data.get('ReleaseDate'))
    return jsonify({"GameID": game.GameID, "GameName": game.GameName, "PublisherID": game.PublisherID, "ReleaseDate": game.ReleaseDate}), 201

@games_bp.route('/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    data = request.get_json()
    game = GamesService.update_game(game_id, data['GameName'], data['PublisherID'], data.get('ReleaseDate'))
    if game:
        return jsonify({"GameID": game.GameID, "GameName": game.GameName, "PublisherID": game.PublisherID, "ReleaseDate": game.ReleaseDate})
    return jsonify({"error": "Game not found"}), 404

@games_bp.route('/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    success = GamesService.delete_game(game_id)
    if success:
        return jsonify({"message": "Game deleted"}), 204
    return jsonify({"error": "Game not found"}), 404

@games_bp.route('/statistics', methods=['GET'])
def get_game_name_statistics():
    operation = request.args.get('operation', '').upper()
    if operation not in ['MIN', 'MAX', 'AVG', 'COUNT']:
        return jsonify({"error": "Invalid operation. Use one of MIN, MAX, AVG, or COUNT."}), 400

    try:
        result = GamesService.get_game_name_statistics(operation)
        return jsonify({"operation": operation, "result": result}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@games_bp.route('/create-random-tables', methods=['POST'])
def create_random_tables():
    try:
        GamesService.create_random_game_tables()
        return jsonify({"message": "Random tables created successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

