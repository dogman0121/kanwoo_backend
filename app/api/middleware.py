from functools import wraps
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.domain.services.user_service import UserService
from app.infrastructure.repositories import SQLUserRepository
from app.utils import create_response


def login_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_service = UserService(SQLUserRepository())

        user_id = get_jwt_identity()

        user = user_service.get_user_by_id(user_id)
        if not user:
            return create_response(error="unauthorized", detail={"token": "Token not found"}, status_code=401)

        return func(*args, **kwargs)

    return wrapper