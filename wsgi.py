import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, migrate
from App.models import User
from App.main import create_app
from App.controllers import (
    create_user, get_all_users_json, get_all_users, initialize
)
from App.controllers.marker import seed_locations  # ✅ Import your seeding function

# Create the Flask app
app = create_app()

'''
Database Initialization Command
'''

@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')

'''
User Commands
'''

user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)

'''
Marker Commands
'''

marker_cli = AppGroup('marker', help='Marker (location) commands')

@marker_cli.command("seed", help="Seed the location table with sample markers")
def seed_marker_command():
    result = seed_locations()
    print(result)

app.cli.add_command(marker_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)
