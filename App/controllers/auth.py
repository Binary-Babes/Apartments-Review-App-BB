from flask_jwt_extended import (
    create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request
)
from App.models import User
from flask import redirect, url_for

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return create_access_token(identity=username)
    return None

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = User.query.filter_by(username=identity).one_or_none()
        return user.id if user else None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt

def add_auth_context(app):
    from flask_login import current_user
    @app.context_processor
    def inject_user():
        is_authenticated = current_user.is_authenticated
        return dict(
            is_authenticated=is_authenticated,
            current_user=current_user,
            is_admin=getattr(current_user, 'is_admin', False)
        )


