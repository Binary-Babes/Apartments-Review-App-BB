

from flask import Blueprint, request, jsonify
from flask_login import login_required  
from App.database import db
from App.models.location import Location

marker_views = Blueprint('marker_views', __name__)

@marker_views.route('/map-data')
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

@marker_views.route('/add-marker', methods=['POST'])
@login_required  
def add_marker():
    data = request.get_json()
    try:
        new_marker = Location(
            name=data['name'],
            lat=data['lat'],
            lng=data['lng'],
            faculty=data['faculty'],
            type=data['type']
        )
        db.session.add(new_marker)
        db.session.commit()
        return jsonify({"message": "Marker added successfully"}), 201
    except Exception as e:
        print("Add marker error:", e)
        return jsonify({"error": "Could not add marker"}), 400

@marker_views.route('/delete-marker/<int:id>', methods=['DELETE'])
@login_required  
def delete_marker(id):
    marker = Location.query.get(id)
    if not marker:
        return jsonify({"error": "Marker not found"}), 404
    try:
        db.session.delete(marker)
        db.session.commit()
        return jsonify({"message": "Marker deleted"}), 200
    except Exception as e:
        print("Delete marker error:", e)
        return jsonify({"error": "Could not delete marker"}), 400


@marker_views.route('/seed')
def seed_locations():
    sample_locations = [
        Location(name="Admin Building", lat=10.6415, lng=-61.3992, faculty="FST", type="building"),
        Location(name="Engineering Block A", lat=10.6421, lng=-61.4010, faculty="ENG", type="classroom"),
        Location(name="Library", lat=10.6400, lng=-61.3985, faculty="FSS", type="building"),
    ]
    db.session.bulk_save_objects(sample_locations)
    db.session.commit()
    return f"{len(sample_locations)} locations seeded!"
