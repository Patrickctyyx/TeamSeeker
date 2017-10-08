from flask_restful import Resource
from .item_parser import item_post_api
from app.models import db, User, Item, Project, Competition


class ItemApi(Resource):

    def get(self):
        pass

    def post(self):

        args = item_post_api.parse_args()
        user = User.verify_auth_token(args['token'])
        if not user:
            return {
                       'errcode': 2,
                       'msg': 'invalid token!'
                   }, 403

        check_item = Item.query.filter_by(requires=args['requires']).first()
        if check_item:
            flag = False
            if check_item.type == 1:
                if check_item.project.tea_id == user.openid:
                    flag = True
            else:
                if check_item.competition.publisher_id == user.openid:
                    flag = True
            if flag:
                return {
                    'errcode': 11,
                    'msg': 'duplicate items!'
                }

        item = Item()
        item.type = args['type']
        item.num = args.get('num')
        item.ddl = args.get('ddl')
        item.requires = args['requires']

        db.session.add(item)
        db.session.flush()

        if item.type == 1:
            if user.identity != 1:
                return {
                    'errcode': 8,
                    'msg': 'permission denied!'
                }, 403
            if not args.get('theme'):
                return {
                    'errcode': 9,
                    'msg': 'theme can not be empty!'
                }, 403
            item_info = Project(id=item.id)
            item_info.tea_id = user.openid
            item_info.theme = args['theme']
            item_info.introduction = args['introduction']
        else:
            if user.identity != 0:
                return {
                    'errcode': 8,
                    'msg': 'permission denied'
                }, 403
            if not args.get('comp_name'):
                return {
                    'errcode': 10,
                    'msg': 'comp_name can not be empty!'
                }, 403
            item_info = Competition(id=item.id)
            item_info.comp_name = args['comp_name']
            item_info.publisher_id = user.openid

        db.session.add(item_info)
        db.session.commit()

        return {'msg': 'ok'}, 200

    def put(self):
        pass

    def delete(self):
        pass
