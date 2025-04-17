# App/controllers/marker.py
from App.database import db
from App.models.location import Location

def seed_locations():
    sample_locations = [
        Location(name="Admin Building", lat=10.6415, lng=-61.3992, faculty="FST", type="building"),
        Location(name="Engineering Block A", lat=10.6421, lng=-61.4010, faculty="ENG", type="classroom"),
        Location(name="Library", lat=10.6400, lng=-61.3985, faculty="FSS", type="building"),
    ]
    db.session.bulk_save_objects(sample_locations)
    db.session.commit()
    return f"{len(sample_locations)} locations seeded!"
