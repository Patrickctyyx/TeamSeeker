from flask_restful import Resource
from .item_parser import item_post_api, item_put_api
from app.models import db, User, Item, Project, Competition
from app.errors import (
    InvalidToken,
    DuplicateInfo,
    PermissionNotMatch,
    LackOfInfo
)


class ItemApi(Resource):

    def get(self):
        pass

    def post(self):

        args = item_post_api.parse_args()
        user = User.verify_auth_token(args['token'])
        if not user:
            raise InvalidToken()

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
                raise DuplicateInfo('items')

        item = Item()
        item.type = args['type']
        item.num = args.get('num')
        item.ddl = args.get('ddl')
        item.requires = args['requires']

        db.session.add(item)
        db.session.flush()

        if item.type == 1:
            if user.identity != 1:
                raise PermissionNotMatch()
            if not args.get('theme'):
                raise LackOfInfo('theme')
            item_info = Project(id=item.id)
            item_info.tea_id = user.openid
            item_info.theme = args['theme']
            item_info.introduction = args['introduction']
        else:
            if user.identity != 0:
                raise PermissionNotMatch()
            if not args.get('comp_name'):
                raise LackOfInfo('comp_name')
            item_info = Competition(id=item.id)
            item_info.comp_name = args['comp_name']
            item_info.publisher_id = user.openid

        db.session.add(item_info)
        db.session.commit()

        return {'msg': 'ok'}, 200

    def put(self):

        args = item_put_api.parse_args()
        user = User.verify_auth_token(args['token'])

        if not user:
            raise InvalidToken()

        item = Item.query.get(args['id'])
        if not item:
            raise LackOfInfo('item')
        item.num = args.get('num')
        item.status = args.get('status')
        item.ddl = args.get('ddl')
        item.requires = args['requires']

        if item.type == 1:
            if not args.get('theme'):
                raise LackOfInfo('theme')
            item.project.theme = args['theme']
            item.project.introduction = args.get('introduction')
        else:
            if not args.get('comp_name'):
                raise LackOfInfo('comp_name')
            item.competition.comp_name = args['comp_name']

        db.session.add(item)
        db.session.commit()
        return {'msg': 'ok'}, 200

    def delete(self):
        pass
