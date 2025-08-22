from functools import wraps

from app.exceptions import HTTPUnauthorized
from app.user.utils import get_current_user


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_current_user()

        if user_id is None:
            raise HTTPUnauthorized({"token": ["Missing authorization token"]})
        return func(*args, **kwargs)

    return wrapper
