from flask import jsonify
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from config import app_config
from api.views import api
from api.models import db, Users, Projects, Bids


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    db.init_app(app)
    app.register_blueprint(api)

    return app
