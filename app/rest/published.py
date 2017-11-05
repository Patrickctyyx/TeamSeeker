import operator
from flask_restful import Resource, reqparse
from app.models import User, Competition
from app.errors import ObjectNotFound


class PublishedApi(Resource):

    def get(self):
        published_get_api = reqparse.RequestParser()
        published_get_api.add_argument(
            'publisher_id',
            type=str,
            required=True
        )
        args = published_get_api.parse_args()

        user = User.query.get(args['publisher_id'])
        if not user:
            raise ObjectNotFound('user')
        if user.identity == 1:
            posts = user.teacher.projects.all()
        else:
            posts = Competition.query.filter_by(
                publisher_id=user.openid
            ).all()

        cmpfun = operator.attrgetter('item.cred_at')
        posts.sort(key=cmpfun, reverse=True)

        result_list = list()
        for post in posts:
            result = dict()
            item = post.item
            result['id'] = item.id
            result['type'] = item.type
            result['num'] = item.num
            result['status'] = item.status
            result['ddl'] = item.ddl
            result['requires'] = item.requires
            result['cred_at'] = str(item.cred_at)
            result['last_modified'] = str(item.last_modified)

            if item.type == 1:
                result['tea_id'] = post.tea_id
                result['theme'] = post.theme
                result['introduction'] = post.introduction
            else:
                result['comp_name'] = post.comp_name
                result['publisher_id'] = post.publisher_id

            result_list.append(result)

        return result_list, 200

