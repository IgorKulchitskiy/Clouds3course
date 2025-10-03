from flask import Blueprint, request, jsonify
from t08_flask_mysql.app.my_project.service.publishers_service import PublishersService

publishers_bp = Blueprint('publishers', __name__)

@publishers_bp.route('/', methods=['GET'])
def get_all_publishers():
    """
    Get all publishers
    ---
    tags:
      - Publishers
    responses:
      200:
        description: "List of all publishers"
        schema:
          type: array
          items:
            type: object
            properties:
              PublisherID:
                type: integer
              PublisherName:
                type: string
    """
    publishers = PublishersService.get_all_publishers()
    return jsonify([{"PublisherID": p.PublisherID, "PublisherName": p.PublisherName} for p in publishers])


@publishers_bp.route('/<int:publisher_id>', methods=['GET'])
def get_publisher_by_id(publisher_id):
    """
    Get a publisher by ID
    ---
    tags:
      - Publishers
    parameters:
      - name: publisher_id
        in: path
        type: integer
        required: true
        description: "ID of the publisher"
    responses:
      200:
        description: "Publisher found"
        schema:
          type: object
          properties:
            PublisherID:
              type: integer
            PublisherName:
              type: string
      404:
        description: "Publisher not found"
    """
    publisher = PublishersService.get_publisher_by_id(publisher_id)
    if publisher:
        return jsonify({"PublisherID": publisher.PublisherID, "PublisherName": publisher.PublisherName})
    return jsonify({"error": "Publisher not found"}), 404


@publishers_bp.route('/', methods=['POST'])
def create_publisher():
    """
    Create a new publisher
    ---
    tags:
      - Publishers
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            PublisherName:
              type: string
    responses:
      201:
        description: "Publisher created"
        schema:
          type: object
          properties:
            PublisherID:
              type: integer
            PublisherName:
              type: string
    """
    data = request.get_json()
    publisher = PublishersService.create_publisher(data['PublisherName'])
    return jsonify({"PublisherID": publisher.PublisherID, "PublisherName": publisher.PublisherName}), 201


@publishers_bp.route('/<int:publisher_id>', methods=['PUT'])
def update_publisher(publisher_id):
    """
    Update a publisher by ID
    ---
    tags:
      - Publishers
    parameters:
      - name: publisher_id
        in: path
        type: integer
        required: true
        description: "ID of the publisher"
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            PublisherName:
              type: string
    responses:
      200:
        description: "Publisher updated"
        schema:
          type: object
          properties:
            PublisherID:
              type: integer
            PublisherName:
              type: string
      404:
        description: "Publisher not found"
    """
    data = request.get_json()
    publisher = PublishersService.update_publisher(publisher_id, data['PublisherName'])
    if publisher:
        return jsonify({"PublisherID": publisher.PublisherID, "PublisherName": publisher.PublisherName})
    return jsonify({"error": "Publisher not found"}), 404


@publishers_bp.route('/<int:publisher_id>', methods=['DELETE'])
def delete_publisher(publisher_id):
    """
    Delete a publisher by ID
    ---
    tags:
      - Publishers
    parameters:
      - name: publisher_id
        in: path
        type: integer
        required: true
        description: "ID of the publisher"
    responses:
      204:
        description: "Publisher deleted"
      404:
        description: "Publisher not found"
    """
    success = PublishersService.delete_publisher(publisher_id)
    if success:
        return jsonify({"message": "Publisher deleted"}), 204
    return jsonify({"error": "Publisher not found"}), 404


@publishers_bp.route('/<int:publisher_id>/games', methods=['GET'])
def get_games_by_publisher(publisher_id):
    """
    Get games by publisher ID
    ---
    tags:
      - Publishers
    parameters:
      - name: publisher_id
        in: path
        type: integer
        required: true
        description: "ID of the publisher"
    responses:
      200:
        description: "List of games for the publisher"
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
      404:
        description: "No games found for this publisher"
    """
    games = PublishersService.get_games_by_publisher(publisher_id)
    if games:
        return jsonify([{"GameID": g.GameID, "GameName": g.GameName, "PublisherID": g.PublisherID, "ReleaseDate": g.ReleaseDate} for g in games])
    return jsonify({"error": "No games found for this publisher"}), 404


@publishers_bp.route('/create-noname-publishers', methods=['POST'])
def create_noname_publishers():
    """
    Create noname publishers starting from a number
    ---
    tags:
      - Publishers
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            startNum:
              type: integer
    responses:
      201:
        description: "Noname publishers created"
      400:
        description: "Missing startNum"
      500:
        description: "Internal server error"
    """
    data = request.get_json()
    start_num = data.get('startNum')
    if start_num is None:
        return jsonify({"error": "startNum is required"}), 400
    try:
        PublishersService.create_noname_publishers(start_num)
        return jsonify({"message": "Noname publishers created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
