from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.set_password(password)
        self.is_admin = is_admin

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin
        }

   
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
