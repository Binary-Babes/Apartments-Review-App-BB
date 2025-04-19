# App/controllers/marker.py

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
        Location(name="SALISES", lat=10.6419421, lng=-61.4009943, faculty="LAW", type="Building"),
        Location(name="FSS UNDERCROFT", lat=10.6397822, lng=-61.3985502, faculty="FSS", type="Common Area"),
        Location(name="Alma Jordan Library", lat=10.6396599, lng=-61.3990611, faculty="Other", type="Building"),
        Location(name="Canada Hall", lat=10.6383258, lng=-61.3969247, faculty="Other", type="Residency"),
        Location(name="Civil Engineering ", lat=10.6388559, lng=-61.3997330, faculty="ENG", type="Building"),
        Location(name="FST 114", lat=10.6407032, lng= -61.4000827, faculty="FST", type="Classroom"),
        Location(name="Undergraduate CSL", lat=10.6413556, lng=-61.4008314, faculty="FST", type="Lab"),
        Location(name="Engineering Workshops", lat=10.6387709, lng=-61.4004197, faculty="ENG", type="Classroom"),
        Location(name="Dudley Huggins Building", lat=10.6450613, lng=-61.4007673, faculty="Other", type="Building"),
        Location(name="TGR Student Carpark", lat=10.6435053, lng=-61.4028062, faculty="Other", type="Carpark"),
    ]
    db.session.bulk_save_objects(sample_locations)
    db.session.commit()
    return f"{len(sample_locations)} locations seeded!"


def initialize_markers(app):
    with app.app_context():
        seed_locations()
