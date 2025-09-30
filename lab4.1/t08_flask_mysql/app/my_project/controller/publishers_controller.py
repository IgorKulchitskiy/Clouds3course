from flask import Blueprint, request, jsonify
from t08_flask_mysql.app.my_project.service.publishers_service import PublishersService

publishers_bp = Blueprint('publishers', __name__)

@publishers_bp.route('/', methods=['GET'])
def get_all_publishers():
    publishers = PublishersService.get_all_publishers()
    return jsonify([{"PublisherID": p.PublisherID, "PublisherName": p.PublisherName} for p in publishers])

@publishers_bp.route('/<int:publisher_id>', methods=['GET'])
def get_publisher_by_id(publisher_id):
    publisher = PublishersService.get_publisher_by_id(publisher_id)
    if publisher:
        return jsonify({"PublisherID": publisher.PublisherID, "PublisherName": publisher.PublisherName})
    return jsonify({"error": "Publisher not found"}), 404

@publishers_bp.route('/', methods=['POST'])
def create_publisher():
    data = request.get_json()
    publisher = PublishersService.create_publisher(data['PublisherName'])
    return jsonify({"PublisherID": publisher.PublisherID, "PublisherName": publisher.PublisherName}), 201

@publishers_bp.route('/<int:publisher_id>', methods=['PUT'])
def update_publisher(publisher_id):
    data = request.get_json()
    publisher = PublishersService.update_publisher(publisher_id, data['PublisherName'])
    if publisher:
        return jsonify({"PublisherID": publisher.PublisherID, "PublisherName": publisher.PublisherName})
    return jsonify({"error": "Publisher not found"}), 404

@publishers_bp.route('/<int:publisher_id>', methods=['DELETE'])
def delete_publisher(publisher_id):
    success = PublishersService.delete_publisher(publisher_id)
    if success:
        return jsonify({"message": "Publisher deleted"}), 204
    return jsonify({"error": "Publisher not found"}), 404


@publishers_bp.route('/<int:publisher_id>/games', methods=['GET'])
def get_games_by_publisher(publisher_id):
    games = PublishersService.get_games_by_publisher(publisher_id)
    if games:
        return jsonify([{"GameID": g.GameID, "GameName": g.GameName, "PublisherID": g.PublisherID, "ReleaseDate": g.ReleaseDate} for g in games])
    return jsonify({"error": "No games found for this publisher"}), 404

@publishers_bp.route('/create-noname-publishers', methods=['POST'])
def create_noname_publishers():
    data = request.get_json()
    start_num = data.get('startNum')
    if start_num is None:
        return jsonify({"error": "startNum is required"}), 400
    try:
        PublishersService.create_noname_publishers(start_num)
        return jsonify({"message": "Noname publishers created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
