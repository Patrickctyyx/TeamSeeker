class ApiError(Exception):
    errcode = 0
    msg = ''

    def __init__(self, msg=''):
        self.msg = msg

    @property
    def data(self):
        return {
            'errcode': self.errcode,
            'msg': self.msg
        }


class InvalidJSCode(ApiError):
    errcode = 1

    def __init__(self, info):
        self.msg = {
            'msg': 'invalid js code!',
            'detail': info
        }


class InvalidToken(ApiError):
    errcode = 2

    def __init__(self):
        self.msg = 'invalid token!'


class LackOfInfo(ApiError):
    errcode = 3

    def __init__(self, info):
        self.msg = 'lack of {}!'.format(info)


class DuplicateInfo(ApiError):
    errcode = 4

    def __init__(self, info):
        self.msg = 'duplicate {}!'.format(info)


class ObjectNotFound(ApiError):
    errcode = 5

    def __init__(self, info):
        self.msg = '{} does not exist!'.format(info)


class PermissionNotMatch(ApiError):
    errcode = 6

    def __init__(self):
        self.msg = 'permission does not match identity!'
