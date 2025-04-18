import os

def load_config(app, overrides):
    if os.path.exists(os.path.join('./App', 'custom_config.py')):
        app.config.from_object('App.custom_config')
    else:
        app.config.from_object('App.default_config')

    app.config.from_prefixed_env()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'

    # ✅ Corrected for UploadSet name = 'uploads'
    app.config['UPLOADED_UPLOADS_DEST'] = "App/uploads"

    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # Set to 1 hour or adjust as needed
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'postgresql://uwi_maps_db_user:38PY1JiZQJm8Ik5P6vxuDnWb41adWAzA@<IP_ADDRESS>/uwi_maps_db'
    )

    for key in overrides:
        app.config[key] = overrides[key]
