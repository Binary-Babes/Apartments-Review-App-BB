from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.models.location import Location
from App.models.user import User
from App.database import db

map_views = Blueprint('map_views', __name__)

@map_views.route('/map-data')
def map_data():
    markers = Location.query.all()
    return jsonify([
        {
            "id": m.id,
            "name": m.name,
            "lat": m.lat,
            "lng": m.lng,
            "faculty": m.faculty,
            "type": m.type
        }
        for m in markers
    ])

@map_views.route('/add-marker', methods=['POST'])
@jwt_required()
def add_marker():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    new_marker = Location(
        name=data['name'],
        lat=data['lat'],
        lng=data['lng'],
        faculty=data['faculty'],
        type=data['type']
    )
    db.session.add(new_marker)
    db.session.commit()
    return jsonify({'message': 'Marker added successfully'}), 200

@map_views.route('/delete-marker/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_marker(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    marker = Location.query.get(id)
    if not marker:
        return jsonify({'error': 'Marker not found'}), 404

    db.session.delete(marker)
    db.session.commit()
    return jsonify({'message': 'Marker deleted successfully'}), 200
