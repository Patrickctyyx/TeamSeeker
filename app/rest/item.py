from flask_restful import Resource
from .item_parser import item_post_api, item_put_api, item_delete_api
from app.models import db, User, Item, Project, Competition
from app.errors import (
    InvalidToken,
    DuplicateInfo,
    PermissionNotMatch,
    LackOfInfo,
    ObjectNotFound
)


class ItemApi(Resource):

    def get(self, item_id=None):

        if not item_id:
            raise LackOfInfo('item id')
        item = Item.query.get(item_id)
        if not item:
            raise ObjectNotFound('item')

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

        return result, 200, {'Access-Control-Allow-Origin': '*'}

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
            if not args.get('theme') or not args.get('introduction'):
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

        return {'msg': 'ok'}, 200, {'Access-Control-Allow-Origin': '*'}

    def put(self):

        args = item_put_api.parse_args()
        user = User.verify_auth_token(args['token'])

        if not user:
            raise InvalidToken()

        item = Item.query.get(args['id'])
        if not item:
            raise ObjectNotFound('item')

        if item.type == 1:
            creater_id = item.project.tea_id
        else:
            creater_id = item.competition.publisher_id

        if creater_id != user.openid:
            raise PermissionNotMatch()

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
        return {'msg': 'ok'}, 200, {'Access-Control-Allow-Origin': '*'}

    def delete(self, item_id=None):

        args = item_delete_api.parse_args()

        user = User.verify_auth_token(args['token'])
        if not user:
            raise InvalidToken()
        if not item_id:
            raise LackOfInfo('item id')
        item = Item.query.get(item_id)
        if not item:
            raise ObjectNotFound('item')

        if item.type == 1:
            creater_id = item.project.tea_id
            item_info = item.project
        else:
            creater_id = item.competition.publisher_id
            item_info = item.competition

        if creater_id != user.openid:
            raise PermissionNotMatch()

        db.session.delete(item_info)
        db.session.delete(item)
        db.session.commit()

        return {'msg': 'ok'}, 200, {'Access-Control-Allow-Origin': '*'}
