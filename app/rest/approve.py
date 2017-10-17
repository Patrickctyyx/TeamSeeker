from flask_restful import Resource
from .approve_parser import approve_post_parser, approve_get_parser
from app.models import db, User, Application, Item, Project, Competition, Student
from app.errors import (
    InvalidToken,
    PermissionNotMatch,
    DuplicateInfo,
    LackOfInfo,
    ObjectNotFound
)


class ApproveApi(Resource):

    def get(self):
        # args = approve_get_parser.parse_args()
        # user = User.verify_auth_token(args['token'])
        # if not user:
        #     raise InvalidToken()
        #
        # result = list()
        #
        # if args.get['status'] is None:
        #     applications = Application.query.filter_by(
        #         item_id=args['item_id']
        #     ).all()
        #     info = dict()
        #     for
        pass

    def post(self):
        args = approve_post_parser.parse_args()
        user = User.verify_auth_token(args['token'])
        if not user:
            raise InvalidToken()

        application = Application.query.get(args['apply_id'])
        if not application:
            raise ObjectNotFound('application')

        item = Item.query.get(application.item_id)
        if not item:
            # Maybe the item has been deleted.
            raise ObjectNotFound('item')

        if user.identity != item.type:
            raise PermissionNotMatch()

        application.status = args['result']

        if args['result'] == 1:
            student = Student.query.get(application.stu_id)
            if item.type == 0:
                comp = item.competition
                student.competitions.append(comp)
            else:
                proj = item.project
                student.projects.append(proj)
            db.session.add(student)

        db.session.add(application)
        db.session.commit()

        return {'msg': 'ok'}, 200
