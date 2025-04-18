from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_user, unset_jwt_cookies, set_access_cookies
from flask_login import login_user, logout_user, current_user
from App.models.user import User
from App.controllers import login as jwt_login

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
SESSION-BASED LOGIN FOR FRONTEND
'''
@auth_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('index_views.index_page'))
    else:
        flash('Invalid credentials')
        return render_template('login.html')

@auth_views.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))


'''
Page/Action Routes (JWT PROTECTED)
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    # You can replace this with your actual user fetch logic
    return render_template('users.html', users=[])

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {jwt_user.id} - {jwt_user.username}")
    

@auth_views.route('/legacy-login', methods=['POST'])  # Renamed to avoid conflict
def login_action():
    data = request.form
    token = jwt_login(data['username'], data['password'])
    response = redirect(request.referrer)
    if not token:
        flash('Bad username or password given'), 401
    else:
        flash('Login Successful')
        set_access_cookies(response, token) 
    return response

@auth_views.route('/legacy-logout', methods=['GET'])  # Renamed to avoid conflict
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = jwt_login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {jwt_user.username}, id : {jwt_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response
