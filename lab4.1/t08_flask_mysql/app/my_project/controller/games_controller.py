from flask import Blueprint, request, jsonify
from t08_flask_mysql.app.my_project.service.games_service import GamesService

games_bp = Blueprint('games', __name__)


@games_bp.route('/', methods=['GET'])
def get_all_games():
    """
    Gett full games
    ---
    tags:
      - Games
    responses:
      200:
        description: "List of all games"
        schema:
          type: array
          items:
            type: object
            properties:
              GameID:
                type: integer
              GameName:
                type: string
              PublisherID:
                type: integer
              ReleaseDate:
                type: string
    """
    games = GamesService.get_all_games()
    return jsonify(
        [{"GameID": g.GameID, "GameName": g.GameName, "PublisherID": g.PublisherID, "ReleaseDate": g.ReleaseDate} for g
         in games])


@games_bp.route('/<int:game_id>', methods=['GET'])
def get_game_by_id(game_id):
    """
    Get a game by ID
    ---
    tags:
      - Games
    parameters:
      - name: game_id
        in: path
        type: integer
        required: true
        description: "ID of the game"
    responses:
      200:
        description: "Game found"
        schema:
          type: object
          properties:
            GameID:
              type: integer
            GameName:
              type: string
            PublisherID:
              type: integer
            ReleaseDate:
              type: string
      404:
        description: "Game not found"
    """
    game = GamesService.get_game_by_id(game_id)
    if game:
        return jsonify({"GameID": game.GameID, "GameName": game.GameName, "PublisherID": game.PublisherID,
                        "ReleaseDate": game.ReleaseDate})
    return jsonify({"error": "Game not found"}), 404


@games_bp.route('/', methods=['POST'])
def create_game():
    """
    Create a new game
    ---
    tags:
      - Games
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            GameName:
              type: string
            PublisherID:
              type: integer
            ReleaseDate:
              type: string
    responses:
      201:
        description: "Game created"
        schema:
          type: object
          properties:
            GameID:
              type: integer
            GameName:
              type: string
            PublisherID:
              type: integer
            ReleaseDate:
              type: string
    """
    data = request.get_json()
    game = GamesService.create_game(data['GameName'], data['PublisherID'], data.get('ReleaseDate'))
    return jsonify({"GameID": game.GameID, "GameName": game.GameName, "PublisherID": game.PublisherID,
                    "ReleaseDate": game.ReleaseDate}), 201




@games_bp.route('/statistics', methods=['GET'])
def get_game_name_statistics():
    """
    Get statistics of game names (MIN, MAX, AVG, COUNT)
    ---
    tags:
      - Games
    parameters:
      - name: operation
        in: query
        type: string
        required: true
        description: "Operation type (MIN, MAX, AVG, COUNT)"
    responses:
      200:
        description: "Statistics result"
        schema:
          type: object
          properties:
            operation:
              type: string
            result:
              type: number
      400:
        description: "Invalid operation"
    """
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
    """
    Create random game tables
    ---
    tags:
      - Games
    responses:
      201:
        description: "Random tables created successfully"
      500:
        description: "Internal server error"
    """
    try:
        GamesService.create_random_game_tables()
        return jsonify({"message": "Random tables created successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
