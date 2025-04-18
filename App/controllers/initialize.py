from App.controllers.user import create_user
from App.database import db

def initialize(app):
    with app.app_context():  # ✅ Use passed-in app context
        db.drop_all()
        db.create_all()

        create_user("bob", "bobpass", is_admin=True)
        create_user("prem", "prempass", is_admin=False)

        print("[INIT] Created default users: bob (admin), prem (user)")
