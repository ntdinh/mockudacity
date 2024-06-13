from functools import wraps
from flask_jwt_extended import verify_jwt_in_request


def loggedRequired(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        return func(*args, **kwargs)
    return decorated
