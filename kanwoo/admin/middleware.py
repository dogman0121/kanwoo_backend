from functools import wraps

from kanwoo.exceptions import ApiForbidden
from kanwoo.profile.middleware import profile_required

def role_required(min_role: int = 0):
    """ Check if profile role more than min_role """
    if min_role < 0:
        raise ValueError("Min role can't be negagive.")

    def decorator(func):
        @wraps(func)
        @profile_required()
        def wrapper(profile, *args, **kwargs):
            if profile.role < min_role:
                raise ApiForbidden(status_code=403, detail={"role": ["Your role is too low."]})

            return func(profile, *args, **kwargs)
        return wrapper
    return decorator

def moderator_required(func):
    return role_required(10)(func)

def admin_required(func):
    return role_required(20)(func)