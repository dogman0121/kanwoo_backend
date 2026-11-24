from functools import wraps
from flask import request, g
from dependency_injector.wiring import inject, Provide

from kanwoo.containers import AppContainer
from kanwoo.exceptions import ApiUnauthorized
from kanwoo.auth.middleware import login_required
from kanwoo.profile.permissions import ProfileAuthPolicy
from kanwoo.profile.services import ProfileAuthService
from kanwoo.profile.exceptions import ProfileNotFoundException
from kanwoo.profile.entity import AnonymousProfile, DebugProfile
from kanwoo.user.entity import DebugUser

def profile_required(optional=False, csrf_protect=True):
    def decorator(func):
        @wraps(func)
        @login_required(optional=optional, csrf_protect=csrf_protect)
        @inject
        def wrapper(
            user, 
            *args, 
            profile_auth_service: ProfileAuthService = Provide[AppContainer.profile_container.profile_auth_service],
            profile_auth_policy: ProfileAuthPolicy = Provide[AppContainer.profile_container.profile_auth_policy],
            auth_profile_cookie: str = Provide[AppContainer.config.AUTH_PROFILE_COOKIE_NAME],
            debug: bool = Provide[AppContainer.config.DEBUG],
            **kwargs
        ):
            g.current_profile = AnonymousProfile()

            curr_user = getattr(user, "_get_current_object", lambda: user)()

            if debug and isinstance(curr_user, DebugUser):
                g.current_profile = DebugProfile()
            elif curr_user is None:
                if not optional:
                    raise ApiUnauthorized()
            else:
                profile_id = request.cookies.get(auth_profile_cookie, type=int)

                if profile_id is None:
                    if not optional:
                        raise ApiUnauthorized()
                else:
                    try:
                        profile = profile_auth_service.system_get_profile_by_id(profile_id)

                        if profile_auth_policy.can_use(curr_user, profile):
                            g.current_profile = profile
                        else:
                            if not optional:
                                raise ApiUnauthorized()
        
                    except ProfileNotFoundException:
                        if not optional:
                            raise ApiUnauthorized()
            
            return func(g.current_profile, *args, **kwargs)    
        return wrapper
    return decorator

