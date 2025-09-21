from functools import wraps

from app.exceptions import HTTPUnauthorized
from app.user.utils import get_current_user, get_current_user_or_401


def login_required(func, optional=False, refresh=False):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if optional:
            user_id = get_current_user(refresh=refresh)
        else:
            user_id = get_current_user_or_401(refresh=refresh)

        if user_id is None:
            raise HTTPUnauthorized({"token": ["Missing authorization token"]})
        
        return func(*args, **kwargs)

    return wrapper
