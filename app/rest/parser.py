from flask_restful import reqparse

wxlogin_post_parser = reqparse.RequestParser()
wxlogin_post_parser.add_argument(
    'js_code',
    type=str,
    required=True,
    help='Js code is required to verify user!'
)

authinfo_post_parser = reqparse.RequestParser()
authinfo_post_parser.add_argument(
    'token',
    type=str
)
authinfo_post_parser.add_argument(
    'identity',
    type=int
)
authinfo_post_parser.add_argument(
    'name',
    type=str
)
authinfo_post_parser.add_argument(
    'email',
    type=str
)
authinfo_post_parser.add_argument(
    'university',
    type=str
)
authinfo_post_parser.add_argument(
    'college',
    type=str
)
authinfo_post_parser.add_argument(
    'department',
    type=str
)
authinfo_post_parser.add_argument(
    'introduction',
    type=str
)
authinfo_post_parser.add_argument(
    'p_num',
    type=str
)
authinfo_post_parser.add_argument(
    's_num',
    type=str
)


