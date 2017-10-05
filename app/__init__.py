from flask import Flask
from app.config import config
from app.models import db


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(config[object_name])

    db.init_app(app)

    return app
