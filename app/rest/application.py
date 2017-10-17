from flask_restful import Resource
from .application_parser import application_post_put_parser, application_delete_parser
from app.models import db, User, Application
from app.errors import (
    InvalidToken,
    PermissionNotMatch,
    DuplicateInfo,
    LackOfInfo,
    ObjectNotFound
)


class ApplicationApi(Resource):

    def get(self, item_id=None):
        if not item_id:
            raise LackOfInfo('item id')

        applications = Application.query.filter_by(item_id=item_id).all()
        if not applications:
            return {'applications': []}, 200

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

        return {'applications': result_list}, 200

    def post(self):
        args = application_post_put_parser.parse_args()
        user = User.verify_auth_token(args['token'])
        if not user:
            raise InvalidToken()

        if user.identity != 0:
            raise PermissionNotMatch()

        apply = Application.query.filter_by(
            item_id=args['item_id'],
            stu_id=user.openid
        ).first()
        if apply:
            raise DuplicateInfo('application')

        apply = Application()
        apply.stu_id = user.openid
        apply.item_id = args['item_id']
        apply.content = args['content']

        db.session.add(apply)
        db.session.commit()

        return {'msg': 'ok'}, 200

    def put(self):
        args = application_post_put_parser.parse_args()
        user = User.verify_auth_token(args['token'])
        if not user:
            raise InvalidToken()

        if user.identity != 0:
            raise PermissionNotMatch()

        apply = Application.query.filter_by(
            item_id=args['item_id'],
            stu_id=user.openid
        ).first()
        if not apply:
            raise ObjectNotFound('application')

        apply.content = args['content']

        db.session.add(apply)
        db.session.commit()

        return {'msg': 'ok'}, 200

    def delete(self, item_id=None):

        args = application_delete_parser.parse_args()
        user = User.verify_auth_token(args['token'])
        if not user:
            raise InvalidToken()

        if not item_id:
            raise LackOfInfo('item id')

        apply = Application.query.filter_by(
            item_id=item_id,
            stu_id=user.openid
        ).first()

        db.session.delete(apply)
        db.session.commit()

        return {'msg': 'ok'}, 200
