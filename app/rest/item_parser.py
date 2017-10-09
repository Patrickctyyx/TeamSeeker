from flask_restful import reqparse
from app.utils import status_type

item_post_api = reqparse.RequestParser()
item_post_api.add_argument(
    'token',
    type=str,
    required=True
)
item_post_api.add_argument(
    'type',
    type=int,
    required=True
)
item_post_api.add_argument(
    'num',
    type=int
)
item_post_api.add_argument(
    'status',
    type=status_type,
    required=True
)
item_post_api.add_argument(
    'ddl',
    type=str
)
item_post_api.add_argument(
    'requires',
    type=str,
    required=True
)
# if it's a Project
item_post_api.add_argument(
    'tea_id',
    type=str
)
item_post_api.add_argument(
    'theme',
    type=str
)
item_post_api.add_argument(
    'introduction',
    type=str
)
# if it's a competition
item_post_api.add_argument(
    'comp_name',
    type=str
)

item_put_api = reqparse.RequestParser()
item_put_api.add_argument(
    'token',
    type=str,
    required=True
)
item_put_api.add_argument(
    'id',
    type=int,
    required=True
)
item_put_api.add_argument(
    'num',
    type=int
)
item_put_api.add_argument(
    'status',
    type=status_type,
    required=True
)
item_put_api.add_argument(
    'ddl',
    type=str
)
item_put_api.add_argument(
    'requires',
    type=str,
    required=True
)
# if it's a Project
item_put_api.add_argument(
    'theme',
    type=str
)
item_put_api.add_argument(
    'introduction',
    type=str
)
# if it's a competition
item_put_api.add_argument(
    'comp_name',
    type=str
)
