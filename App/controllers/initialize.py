from App.controllers.user import create_user
from App.database import db
from App.models.location import Location

def initialize(app):
    with app.app_context(): 
        db.drop_all()
        db.create_all()

        create_user("bob", "bobpass", is_admin=True)
        create_user("prem", "prempass", is_admin=False)

      
        sample_locations = [
            Location(name="SALISES", lat=10.6419421, lng=-61.4009943, faculty="LAW", type="Building"),
            Location(name="Civil Engineering", lat=10.6388559, lng=-61.3997330, faculty="ENG", type="Building"),
            Location(name="Alma Jordan Library", lat=10.6396599, lng=-61.3990611, faculty="Other", type="Building"),
            Location(name="Canada Hall", lat=10.6383258, lng=-61.3969247, faculty="Other", type="Residencey"),
            Location(name="FSS UNDERCROFT", lat=10.6397822, lng=-61.3985502, faculty="FSS", type="Clasroom"),
            Location(name="FST 114", lat=10.6407032, lng=-61.4000827, faculty="FST", type="Building"),
            Location(name="Undergraduate CSL", lat=10.6413556, lng=-61.4008314, faculty="FST", type="Lab"),
            Location(name="Engineering Workshops", lat=10.6387709, lng=-61.4004197, faculty="ENG", type="Classroom"),
            Location(name="Dudley Huggins Building", lat=10.6397822, lng=-61.3985502, faculty="Other", type="Clasroom"),
            Location(name="TGR Student Carpark", lat=10.6435053, lng=-61.4028062, faculty="Other", type="Carpark"),
        ]
        db.session.bulk_save_objects(sample_locations)
        db.session.commit()  

        print("[INIT] Created default users and markers.")
