from typing import Optional

from flask import render_template
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token

from app.auth.exceptions import AuthLoginAlreadyTakenException, AuthEmailAlreadyTakenException, \
    AuthUserWithLoginNotExistException, AuthPasswordNotMatchException, AuthJWTTokenExpiredException, \
    AuthJWTTokenExpiredException, AuthJWTTokenInvalidException
from app.email import EmailService
from app.user.entities import UserEntity
from app.user.exceptions import UserLoginAlreadyTakenException, \
    UserEmailAlreadyTakenException, UserNotFoundException
from app.user.services import UserService

from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time


def _generate_registration_jwt(user_id: int) -> str:
    return jwt.encode({
        "user_id": user_id,
        'exp': time() + 600
    }, key=current_app.config["SECRET_KEY"], algorithm='HS256')

def _check_registration_jwt(token: str) -> Optional[int]:
    try:
        return jwt.decode(token, key=current_app.config["SECRET_KEY"], algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return None

def _create_access_token(user: UserEntity) -> str:
    return create_access_token(user.id)

def _create_refresh_token(user: UserEntity) -> str:
    return create_refresh_token(user.id)

class AuthService:
    @staticmethod
    def register_user(login, email, password) -> None:
        password_hash = generate_password_hash(password)

        try:
            user = UserEntity(
                id=None,
                login=login,
                email=email,
                password=password_hash,
            )

            user = UserService.create_user(user)
            jwt_token = _generate_registration_jwt(user.id)

            EmailService.send_email(
                "Подтверждение почты",
                recipients=[email],
                text=render_template("email/approve_email.txt", token=jwt_token),
                html=render_template("email/approve_email.html", token=jwt_token)
            )
        except UserLoginAlreadyTakenException as e:
            raise AuthLoginAlreadyTakenException(e.args[0])
        except UserEmailAlreadyTakenException as e:
            raise AuthEmailAlreadyTakenException(e.args[0])

    @staticmethod
    def login_user(login: str, password: str) -> [str, str]:
        try:
            user = UserService.get_by_login(login)

            if check_password_hash(user.password, password):
                return _create_access_token(user), _create_refresh_token(user)
            else:
                raise AuthPasswordNotMatchException("Incorrect password.")
        except UserNotFoundException:
            raise AuthUserWithLoginNotExistException("User with this login does not exist.")


    @staticmethod
    def verify_user_registration(token) -> [str, str]:
        user_id = _check_registration_jwt(token)

        if user_id is None:
            raise AuthJWTTokenExpiredException("Verification token is expired.")

        try:
            user = UserService.get_by_id(user_id)

            user.is_verified = True

            user = UserService.update_user(user)

            return _create_access_token(user), create_refresh_token(user)
        except UserNotFoundException:
            raise AuthJWTTokenInvalidException("User with this id does not exist.")





