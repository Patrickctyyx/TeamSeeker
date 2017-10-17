from flask_restful import reqparse
from app.utils import apply_status_type

approve_post_parser = reqparse.RequestParser()
approve_post_parser.add_argument(
    'token',
    type=str,
    required=True
)
# approve_post_parser.add_argument(
#     'item_id',
#     type=int,
#     required=True
# )
approve_post_parser.add_argument(
    'apply_id',
    type=int,
    required=True
)
# result = 1 => ok -1 => rejected
approve_post_parser.add_argument(
    'result',
    type=int,
    required=True
)

approve_get_parser = reqparse.RequestParser()
approve_get_parser.add_argument(
    'token',
    type=str,
    required=True
)
# query by application status
# default => all
approve_get_parser.add_argument(
    'status',
    type=apply_status_type
)
approve_get_parser.add_argument(
    'item_id',
    type=int,
    required=True
)
