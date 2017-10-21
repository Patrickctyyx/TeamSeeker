"""
Content is from https://segmentfault.com/a/1190000000655872
"""

from .names import first_names, last_names
import random
import string


def random_name(size=1, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def first_name(size=2, ln=None, fn=None):
    _lst = []
    for i in range(size):
        _item = random_name(1, fn)
        if ln:
            while _item in ln:
                _item = random_name(1, fn)
            _lst.append(_item)
        else:
            _lst.append(_item)
    return "".join(_lst)


def last_name(size=1, names=None):
    return random_name(size, names)


def full_name(lns, fns):
    _last = last_name(1, lns)
    return "{}{}".format(_last, first_name(random.randint(1, 2), _last, fns))


def get_name():
    return full_name(last_names, first_names)
