from flask_restful import reqparse

application_post_put_parser = reqparse.RequestParser()
application_post_put_parser.add_argument(
    'token',
    type=str,
    required=True
)
application_post_put_parser.add_argument(
    'item_id',
    type=int,
    required=True
)
application_post_put_parser.add_argument(
    'content',
    type=str,
    required=True
)

application_delete_parser = reqparse.RequestParser()
application_delete_parser.add_argument(
    'token',
    type=str,
    required=True
)
