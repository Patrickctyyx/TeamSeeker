from flask import Flask, Response
from app.config import config
from app.models import db
from app.rest.wechat import WeChatLoginApi
from app.rest.auth import AuthApi
from app.rest.application import ApplicationApi
from app.rest.item import ItemApi
from app.rest.approve import ApproveApi
from app.rest.index import IndexApi
from app.rest.published import PublishedApi
from app.rest.received_applications import RcvApplicationApi
from app.rest.sent_applications import SentApplicationApi
from flask_restful import Api
from werkzeug.datastructures import Headers


class MyResponse(Response):
    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')
        # 跨域控制
        origin = ('Access-Control-Allow-Origin', '*')
        methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        if headers:
            headers.add(*origin)
            headers.add(*methods)
        else:
            headers = Headers([origin, methods])
        kwargs['headers'] = headers
        return super().__init__(response, **kwargs)


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(config[object_name])
    app.response_class = MyResponse

    db.init_app(app)

    rest_api = Api()
    rest_api.add_resource(WeChatLoginApi, '/api/wxlogin')
    rest_api.add_resource(
        AuthApi,
        '/api/auth',
        '/api/auth/<string:openid>'
    )
    rest_api.add_resource(
        ItemApi,
        '/api/create',
        '/api/create/<int:item_id>'
    )
    rest_api.add_resource(
        ApplicationApi,
        '/api/apply',
        '/api/apply/<int:item_id>'
    )
    rest_api.add_resource(
        ApproveApi,
        '/api/approve'
    )
    rest_api.add_resource(
        IndexApi,
        '/api/index'
    )
    rest_api.add_resource(
        PublishedApi,
        '/api/published'
    )
    rest_api.add_resource(
        RcvApplicationApi,
        '/api/received'
    )
    rest_api.add_resource(
        SentApplicationApi,
        '/api/sent'
    )
    rest_api.init_app(app)

    return app
