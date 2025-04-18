from App.controllers.user import create_user
from App.database import db
from App.models.location import Location

def initialize(app):
    with app.app_context():  # ✅ Use passed-in app context
        db.drop_all()
        db.create_all()

        create_user("bob", "bobpass", is_admin=True)
        create_user("prem", "prempass", is_admin=False)

        # Seed initial markers
        sample_locations = [
            Location(name="Admin Building", lat=10.6415, lng=-61.3992, faculty="FST", type="building"),
            Location(name="Engineering Block A", lat=10.6421, lng=-61.4010, faculty="ENG", type="classroom"),
            Location(name="Library", lat=10.6400, lng=-61.3985, faculty="FSS", type="building"),
        ]
        db.session.bulk_save_objects(sample_locations)
        db.session.commit()  # Ensure changes are committed to the database

        print("[INIT] Created default users and markers.")
