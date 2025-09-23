from functools import wraps

from app.exceptions import HTTPUnauthorized
from app.user.services import UserService
from app.user.exceptions import UserNotFoundException

from flask_jwt_extended import (verify_jwt_in_request, get_jwt_identity)

def login_required(optional=False, refresh=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request(optional=optional, refresh=refresh)

            user_id = get_jwt_identity()

            if user_id is None:
                raise HTTPUnauthorized({"token": ["Missing authorization token"]})

            try:
                user = UserService.get_by_id(user_id)

                return func(user, *args, **kwargs)
            except UserNotFoundException:
                raise HTTPUnauthorized({"token": ["Invalid token"]})

        return wrapper
    return decorator