from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    JWTManager,
    get_jwt_identity,
    verify_jwt_in_request
)
from flask_login import current_user  # ✅ Use this for session-based context
from App.models import User

# Login function used by the login route or API
def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return create_access_token(identity=username)
    return None

# JWT Setup (still valid for API use if needed)
def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = User.query.filter_by(username=identity).one_or_none()
        if user:
            return user.id
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt

# ✅ Use Flask-Login's current_user for template rendering
def add_auth_context(app):
    @app.context_processor
    def inject_user():
        is_authenticated = current_user.is_authenticated
        return dict(
            is_authenticated=is_authenticated,
            current_user=current_user,
            is_admin=getattr(current_user, 'is_admin', False)
        )
