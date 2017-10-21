import operator
from flask_restful import Resource, reqparse
from app.models import Competition, User
from app.errors import InvalidToken


class RcvApplicationApi(Resource):

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

        applications = list()
        if user.identity == 1:
            items = user.teacher.projects.all()
        else:
            items = Competition.query.filter_by(
                publisher_id=user.openid
            ).all()
        for item in items:
            applications.extend(item.item.applications)

        cmpfun = operator.attrgetter('cred_at')
        applications.sort(key=cmpfun, reverse=True)

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

