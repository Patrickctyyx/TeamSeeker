from flask_restful import Resource, reqparse
from app.models import User, Application
from app.errors import InvalidToken


class SentApplicationApi(Resource):

    def get(self):
        rcv_get_parser = reqparse.RequestParser()
        rcv_get_parser.add_argument(
            'token',
            type=str,
            required=True
        )
        args = rcv_get_parser.parse_args()

        user = User.verify_auth_token(args['token'])
        if not user:
            raise InvalidToken()

        applications = Application.query.filter_by(
            stu_id=user.openid
        ).order_by(Application.cred_at.desc()).all()

        result_list = list()

        for apply in applications:
            result = dict()
            result['id'] = apply.id
            result['stu_id'] = apply.stu_id
            result['item_id'] = apply.item_id
            result['content'] = apply.content
            result['cred_at'] = str(apply.cred_at)
            result['status'] = apply.status
            result_list.append(result)

        return result_list, 200
