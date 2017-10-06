from flask_restful import Resource
from app.models import db, User, Teacher, Student
from .parser import authinfo_post_parser


class AuthApi(Resource):

    def get(self):
        pass

    def post(self):

        args = authinfo_post_parser.parse_args()
        user = User.verify_auth_token(args.get('token'))
        if not user:
            return {'errcode': 2, 'msg': 'invalid token!'}, 403
        identity = user.identity
        if not user.identity and args['identity'] is None:
            return {
                'errcode': 3,
                'msg': 'identity is required for new user!'
            }, 403
        else:
            if args['identity']:
                identity = args['identity']
        if identity == 1:
            user_iden = Teacher.query.get(user.openid)
        else:
            user_iden = Student.query.get(user.openid)
        if not user_iden:
            if identity == 1:
                user_iden = Teacher(openid=user.openid)
            else:
                user_iden = Student(openid=user.openid)
            db.session.add(user_iden)

        for info in args.keys():
            if args[info]:
                if info is 'p_num' or info is 's_num':
                    setattr(user_iden, info, args[info])
                else:
                    setattr(user, info, args[info])

        db.session.commit()

        return {'msg': 'ok'}, 200

