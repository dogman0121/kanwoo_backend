from app.auth.middleware import login_required
from app.exceptions import ApiUnauthorized
from flask import request
from functools import wraps

from .services import ProfileService
from .exceptions import ProfileNotFoundException

def profile_required(optional=False):
    def decorator(func):
        @wraps(func)
        @login_required(optional=optional)
        def wrapper(user, *args, **kwargs):
            if user is None:
                return func(None, *args, **kwargs)    
            
            profile_id = request.cookies.get("auth_profile")

            try:
                profile = ProfileService(user).get_profile_by_id(profile_id)
            except ProfileNotFoundException:
                if optional:
                    return func(None, *args, **kwargs)
                raise ApiUnauthorized

            return func(profile, *args, **kwargs)    
        return wrapper
    return decorator
