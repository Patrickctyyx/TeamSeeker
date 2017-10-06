from flask_restful import reqparse

wxlogin_post_parser = reqparse.RequestParser()
wxlogin_post_parser.add_argument(
    'js_code',
    type=str,
    required=True,
    help='Js code is required to verify user!'
)
