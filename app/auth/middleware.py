from functools import wraps

from app.exceptions import ApiUnauthorized
from app.user.services import UserService
from app.user.exceptions import UserNotFoundException

from flask_jwt_extended import (verify_jwt_in_request, get_jwt_identity)
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import ExpiredSignatureError

def login_required(optional=False, refresh=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request(optional=optional, refresh=refresh)

                user_id = get_jwt_identity()
                
                if user_id is None:
                    if optional:
                        return func(None, *args, **kwargs)
                    raise ApiUnauthorized({"token": ["Missing authorization token"]})
                
                try:
                    user = UserService.get_by_id(user_id)
                    return func(user, *args, **kwargs)
                except UserNotFoundException:
                    if optional:
                        return func(None, *args, **kwargs)
                    raise ApiUnauthorized({"token": ["Invalid token"]})
            except ExpiredSignatureError as e:
                if optional:
                    return func(None, *args, **kwargs)
                raise e
            except JWTExtendedException:
                raise ApiUnauthorized({"token": ["Invalid authorization token"]})
        
        return wrapper
    return decorator