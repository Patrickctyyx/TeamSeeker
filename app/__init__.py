from flask import Flask
from app.config import config
from app.models import db
from app.extensions import rest_api
from app.rest.wechat import WeChatLoginApi
from app.rest.auth import AuthApi


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(config[object_name])

    db.init_app(app)

    rest_api.add_resource(WeChatLoginApi, '/api/wxlogin')
    rest_api.add_resource(
        AuthApi,
        '/api/auth'
    )
    rest_api.init_app(app)

    return app
