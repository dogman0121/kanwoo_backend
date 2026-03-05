from functools import wraps
from datetime import datetime, timezone, timedelta
from flask import request
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    create_access_token,
    set_access_cookies
)
from flask_jwt_extended import (verify_jwt_in_request, get_jwt_identity)
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import ExpiredSignatureError

from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.exceptions import ApiUnauthorized, ApiForbidden
from kanwoo.user.services import UserService
from kanwoo.user.exceptions import UserNotFoundException
from kanwoo.profile.services import ProfileAuthService
from kanwoo.profile.exceptions import ProfileNotFoundException

def login_required(optional=False, refresh=False):
    def decorator(func):
        @wraps(func)
        @inject
        def wrapper(
            *args, 
            user_service: UserService = Provide[AppContainer.user_container.user_service],
            **kwargs
        ):
            try:
                verify_jwt_in_request(optional=optional, refresh=refresh)

                user_id = get_jwt_identity()
                
                if user_id is None:
                    if optional:
                        return func(None, *args, **kwargs)
                    raise ApiUnauthorized(error="token_required", detail={"token": ["Missing authorization token"]})
                
                try:
                    user = user_service.system_get_user_by_id(user_id)

                    return func(user, *args, **kwargs)
                except UserNotFoundException:
                    if optional:
                        return func(None, *args, **kwargs)
                    raise ApiUnauthorized(error="invalid_token", detail={"token": ["Invalid authorization token"]})
            except ExpiredSignatureError as e:
                if optional:
                    return func(None, *args, **kwargs)
                raise e
            except JWTExtendedException:
                raise ApiUnauthorized(error="invalid_token", detail={"token": ["Invalid authorization token"]})
        
        return wrapper
    return decorator

def profile_required(optional=False):
    def decorator(func):
        @wraps(func)
        @login_required(optional=optional)
        @inject
        def wrapper(
            user, 
            *args, 
            profile_auth_service: ProfileAuthService = Provide[AppContainer.profile_container.profile_auth_service],
            **kwargs
        ):
            if user is None:
                return func(None, *args, **kwargs)    
            
            profile_id = request.cookies.get("auth_profile")
            try:
                profile = profile_auth_service.system_get_profile_by_id(profile_id)

                if not profile_auth_service.system_check_user_access_for_profile(user, profile):
                    raise ApiUnauthorized
            except ProfileNotFoundException:
                if optional:
                    return func(None, *args, **kwargs)
                raise ApiUnauthorized

            return func(profile, *args, **kwargs)    
        return wrapper
    return decorator


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

def setup_middleware(app):
    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response