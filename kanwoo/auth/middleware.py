from functools import wraps
from flask import request
from flask_jwt_extended import (
    verify_jwt_in_request, 
    current_user
)
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, jwt_manager 
from kanwoo.exceptions import ApiUnauthorized
from kanwoo.user.services import UserService
from kanwoo.user.exceptions import UserNotFoundException
from kanwoo.user.entity import DebugUser


@jwt_manager.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt_manager.user_lookup_loader
@inject
def user_lookup_callback(
    _jwt_header, 
    jwt_data,
    user_service: UserService = Provide[AppContainer.user_container.user_service]
):
    identity = jwt_data["sub"]
    if identity is None:
        return None

    try:
        return user_service.system_get_user_by_id(identity)
    except UserNotFoundException:
        return None 


def login_required(optional=False, refresh=False, csrf_protect=True):
    def decorator(func):
        @wraps(func)
        @inject
        def wrapper(
            *args, 
            debug: bool = Provide[AppContainer.config.DEBUG],
            **kwargs
        ):
            if debug and request.cookies.get("debug_user_cookie", type=bool):
                debug_user = DebugUser()
                return func(debug_user, *args, **kwargs)

            original_method = request.method
            if not csrf_protect:
                request.method = "GET"

            try:
                verify_jwt_in_request(optional=optional, refresh=refresh)
            except Exception as e:
                raise ApiUnauthorized(f"Invalid token: {str(e)}")
            finally:
                if not csrf_protect:
                    request.method = original_method  # Возвращаем метод обратно

            return func(current_user, *args, **kwargs)
        
        return wrapper
    return decorator
