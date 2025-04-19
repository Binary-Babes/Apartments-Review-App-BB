from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from App.database import db
from App.models.location import Location

map_views = Blueprint('map_views', __name__)

@map_views.route('/map-data')
def get_markers():
    markers = Location.query.all()
    return jsonify([
        {
            "id": m.id,
            "name": m.name,
            "lat": m.lat,
            "lng": m.lng,
            "faculty": m.faculty,
            "type": m.type
        } for m in markers
    ])

@map_views.route('/add-marker', methods=['POST'])
@login_required
def add_marker():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
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
@login_required
def delete_marker(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    marker = Location.query.get(id)
    if not marker:
        return jsonify({'error': 'Marker not found'}), 404

    db.session.delete(marker)
    db.session.commit()  
    return jsonify({'message': 'Marker deleted successfully'}), 200
