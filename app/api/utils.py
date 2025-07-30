from flask import abort
from flask_jwt_extended import get_jwt_identity

from app.domain.services.user_service import UserService
from app.infrastructure.repositories import SQLUserRepository


def get_current_user():
    user_id = get_jwt_identity()

    if user_id is None:
        return None

    user_service = UserService(SQLUserRepository)

    user = user_service.get_user_by_id(user_id)

    return user