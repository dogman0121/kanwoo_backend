from flask import abort
from flask_jwt_extended import (get_jwt_identity, verify_jwt_in_request)
from flask_jwt_extended.exceptions import JWTExtendedException

from kanwoo.user.services import UserService
from kanwoo.user.exceptions import UserNotFoundException


def get_current_user():
    user_id = get_jwt_identity()

    if user_id is None:
        return None

    try:
        user = UserService.get_by_id(user_id)
        return user
    except UserNotFoundException:
        return None

def get_current_user_or_401(refresh=False):
    verify_jwt_in_request(refresh=refresh)

    user_id = get_jwt_identity()

    if user_id is None:
        raise JWTExtendedException

    try:
        user = UserService.get_by_id(user_id)
        return user
    except UserNotFoundException:
        raise JWTExtendedException