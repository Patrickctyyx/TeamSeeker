import requests
import os
from flask_restful import Resource
from .parser import wxlogin_post_parser
from app.models import db, User
from app.errors import InvalidJSCode


class WeChatLoginApi(Resource):

    def post(self):
        args = wxlogin_post_parser.parse_args()
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {
            'appid': os.environ.get('APPID'),
            'secret': os.environ.get('APP_SECRET'),
            'js_code': args['js_code'],
            'grant_type': 'uthorization_code'
        }
        r = requests.get(url, params=payload)
        info = r.json()
        if 'session_key' not in info:
            raise InvalidJSCode(info)
        user = User.query.get(info.get('openid'))
        if not user:
            user = User(openid=info.get('openid'))
            db.session.add(user)
            db.session.commit()
        token = user.generate_auth_token().decode()

        return {'token': token}, 200

