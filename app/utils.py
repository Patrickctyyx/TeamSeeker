import re


def email_type(email):
    if re.match('^[0-9a-zA-Z\_]+@[0-9a-zA-Z\_\.]+\.[a-zA-Z]+$', email):
        return email
    else:
        raise ValueError('Not a proper email!')


def level_type(level):
    if level != 'college' and level != 'master' and level != 'doctor':
        raise ValueError('Not a proper level!')
    return level


def status_type(status):
    if status != 'pending' and status != 'processing' and status != 'ended':
        raise ValueError('Not a proper status!')
    return status


def apply_status_type(status):
    if status != 1 and status != 0 and status != -1:
        raise ValueError('Not a proper status!')
    return status
