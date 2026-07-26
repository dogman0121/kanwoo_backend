from functools import wraps
from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo.containers import AppContainer
from kanwoo.exceptions import ApiUnauthorized
from kanwoo.auth.middleware import login_required
from kanwoo.profile.permissions import ProfileAuthPolicy
from kanwoo.profile.services import ProfileAuthService
from kanwoo.profile.exceptions import ProfileNotFoundException
from kanwoo.profile.entity import AnonymousProfile

def profile_required(optional=False):
    def decorator(func):
        @wraps(func)
        @login_required(optional=optional)
        @inject
        def wrapper(
            user, 
            *args, 
            profile_auth_service: ProfileAuthService = Provide[AppContainer.profile_container.profile_auth_service],
            profile_auth_policy: ProfileAuthPolicy = Provide[AppContainer.profile_container.profile_auth_policy],
            auth_profile_cookie: str = Provide[AppContainer.config.AUTH_PROFILE_COOKIE_NAME],
            **kwargs
        ):
            profile = AnonymousProfile()

            if user is None:
                return func(profile, *args, **kwargs)    
            
            profile_id = request.cookies.get(auth_profile_cookie, type=int)

            

            try:
                profile = profile_auth_service.system_get_profile_by_id(profile_id)

                if not (optional or profile_auth_policy.can_use(user, profile)):
                    raise ApiUnauthorized()
            except ProfileNotFoundException:
                if not optional:
                    raise ApiUnauthorized()

            return func(profile, *args, **kwargs)    
        return wrapper
    return decorator

