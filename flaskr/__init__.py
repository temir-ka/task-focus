import os
from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db',
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from .db import db
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

    from . import auth
    auth.login_manager.init_app(app)
    app.register_blueprint(auth.bp)

    from . import profile
    app.register_blueprint(profile.bp)

    return app
