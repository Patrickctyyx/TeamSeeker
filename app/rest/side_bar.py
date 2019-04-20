from flask_restful import Resource, reqparse
from app.models import Item


class SideBarApi(Resource):

    def get(self):
        # 这个应该是返回比赛的资讯
        # 应该使用爬虫获取信息
        # recent_comp = Item.query.filter_by(
        #     Item.type == 0
        # ).order_by(
        #     Item.last_modified.desc()
        # ).limit(5).all()

        sidebar_get_parser = reqparse.RequestParser()
        sidebar_get_parser.add_argument(
            'type',
            type=int
        )
        args = sidebar_get_parser.parse_args()

        return_type = args.get('type') or 0
        recent = Item.query.order_by(
            Item.cred_at.desc()
        ).filter(Item.type == return_type).limit(5).all()

        result_list = list()

        for item in recent:
            result = dict()
            result['id'] = item.id
            result['type'] = item.type
            result['num'] = item.num
            result['current_num'] = item.current_num
            result['apply_count'] = item.apply_count
            result['status'] = item.status
            result['ddl'] = item.ddl
            result['requires'] = item.requires
            result['cred_at'] = str(item.cred_at)
            result['last_modified'] = str(item.last_modified)

            if return_type == 1:
                result['tea_id'] = item.project.tea_id
                result['theme'] = item.project.theme
                result['introduction'] = item.project.introduction
            else:
                result['comp_name'] = item.competition.comp_name
                result['publisher_id'] = item.competition.publisher_id

            result_list.append(result)

        return result_list, 200
