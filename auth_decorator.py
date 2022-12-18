from flask import session
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('email', None)
        if user:
            return f(*args, **kwargs)
        return "You aren't logged in!"
    return decorated_function