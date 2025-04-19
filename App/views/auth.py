from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from flask_jwt_extended import (
    create_access_token, JWTManager
)
from App.models import User

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@auth_views.route('/login', methods=['POST'])
def login_action():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        flash("Login successful.")
        return redirect(url_for('index_views.index_page'))
    else:
        flash("Invalid username or password.")
        return render_template('login.html')


@auth_views.route('/logout')
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for('auth_views.login_page'))  

def login_jwt(username, password):
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
    @app.context_processor
    def inject_user():
        return dict(
            is_authenticated=current_user.is_authenticated,
            current_user=current_user,
            is_admin=getattr(current_user, 'is_admin', False)
        )

@auth_views.app_errorhandler(401)
def handle_unauthorized(error):
    flash("Session expired. Please log in again.")
    return redirect(url_for('auth_views.login_page'))
