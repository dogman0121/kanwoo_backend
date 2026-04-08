from functools import wraps
from flask import request
from flask_jwt_extended import (
    get_jwt_identity,
)
from flask_jwt_extended import (verify_jwt_in_request, get_jwt_identity)
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import ExpiredSignatureError

from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.exceptions import ApiUnauthorized
from kanwoo.user.services import UserService
from kanwoo.user.exceptions import UserNotFoundException


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
                    user = user_service.system_get_user_by_id(int(user_id))

                    return func(user, *args, **kwargs)
                except UserNotFoundException:
                    if optional:
                        return func(None, *args, **kwargs)
                    raise ApiUnauthorized(error="invalid_token", detail={"token": ["Invalid authorization token"]})
            except ExpiredSignatureError as e:
                if optional:
                    return func(None, *args, **kwargs)
                raise e
            except JWTExtendedException as e:
                raise ApiUnauthorized(error="invalid_token", detail={"token": [str(e)]})
        
        return wrapper
    return decorator