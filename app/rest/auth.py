from flask_restful import Resource
from app.models import db, User, Teacher, Student
from .auth_parser import authinfo_post_parser, authinfo_put_parser
from sqlalchemy.exc import IntegrityError


class AuthApi(Resource):

    def get(self, openid=None):
        if not openid:
            return {
                'errcode': 6,
                'msg': 'openid is necessary to get userinfo!'
            }
        user = User.query.get(openid)
        
        result = dict()
        result['name'] = user.name
        result['email'] = user.email
        result['identity'] = user.identity
        result['university'] = user.university
        result['college'] = user.college
        result['department'] = user.department
        result['introduction'] = user.introduction

        if user.identity == 0:
            student = user.student
            result['level'] = student.level
            result['enter_year'] = student.enter_year

        return result, 200

    def post(self):

        args = authinfo_post_parser.parse_args()
        user = User.verify_auth_token(args['token'])
        if not user:
            return {
                'errcode': 2,
                'msg': 'invalid token!'
            }, 403

        user.identity = args['identity']
        user.name = args['name']
        user.email = args['email']
        user.university = args['university']
        user.college = args['college']
        user.department = args['department']
        user.information = args.get('information')

        if args['identity'] == 1:
            if not args['p_num']:
                return {
                    'errcode': 3,
                    'msg': 'p_num is necessary for a teacher!'
                }, 403

            user_iden = Teacher(
                openid=user.openid,
                p_num=args['p_num']
            )
        else:
            if not args['s_num'] or not args['level'] or not args['enter_year']:
                return {
                    'errcode': 4,
                    'msg': 'student information lacks!'
                }, 403

            user_iden = Student(
                openid=user.openid,
                s_num=args['s_num'],
                level=args['level'],
                enter_year=args['enter_year']
            )
        db.session.add(user_iden)
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            return {
                'errcode': 5,
                'msg': 'duplicated s_num or p_num or email!'
            }, 403

        return {'msg': 'ok'}, 200

    def put(self):

        args = authinfo_put_parser.parse_args()
        user = User.verify_auth_token(args['token'])
        if not user:
            return {
                'errcode': 2,
                'msg': 'invalid token!'
            }, 403

        user.email = args.get('email')
        user.university = args.get('university')
        user.college = args.get('college')
        user.department = args.get('department')
        user.information = args.get('information')

        if user.identity == 0:
            student = user.student
            student.level = args.get('level')
            student.enter_year = args.get('enter_year')
            db.session.add(student)

        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            return {
                'errcode': 5,
                'msg': 'duplicate email!'
            }, 403

        return {'msg': 'ok'}, 200

