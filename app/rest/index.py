from flask_restful import Resource, reqparse
from app.models import Item


class IndexApi(Resource):

    def get(self):
        index_get_parser = reqparse.RequestParser()
        index_get_parser.add_argument(
            'page',
            type=int
        )
        args = index_get_parser.parse_args()

        page = args.get('page') or 1
        items = Item.query.order_by(
            Item.last_modified.desc()
        ).paginate(page, 15).items

        result_list = list()

        for item in items:
            result = dict()
            result['id'] = item.id
            result['type'] = item.type
            result['num'] = item.num
            result['status'] = item.status
            result['ddl'] = item.ddl
            result['requires'] = item.requires
            result['cred_at'] = str(item.cred_at)
            result['last_modified'] = str(item.last_modified)

            if item.type == 1:
                result['tea_id'] = item.project.tea_id
                result['theme'] = item.project.theme
                result['introduction'] = item.project.introduction
            else:
                result['comp_name'] = item.competition.comp_name
                result['publisher_id'] = item.competition.publisher_id

            result_list.append(result)

        return result_list, 200, {'Access-Control-Allow-Origin': '*'}


