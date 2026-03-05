from flask import render_template
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token

from kanwoo.auth.exceptions import AuthEmailAlreadyTakenException, \
    AuthUserWithLoginNotExistException, AuthPasswordNotMatchException, AuthJWTTokenExpiredException, \
    AuthJWTTokenExpiredException, AuthJWTTokenInvalidException, AuthUserWithEmailNotExistException
from kanwoo.email import EmailService
from kanwoo.user.exceptions import UserEmailAlreadyTakenException, UserNotFoundException
from kanwoo.user.models import User
from kanwoo.user.services import UserService

from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time

def _generate_jwt_token(data: dict) -> str:
    return jwt.encode(
        payload=data,
        key=current_app.config["SECRET_KEY"],
        algorithm = 'HS256'
    )

def _check_jwt_token(token: str) -> dict:
    try:
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])

        return data
    except jwt.ExpiredSignatureError:
        raise AuthJWTTokenExpiredException("JWT token is expired.")
    except jwt.InvalidTokenError:
        raise AuthJWTTokenInvalidException("JWT token is invalid.")
    except Exception as e:
        raise AuthJWTTokenInvalidException("JWT token is invalid.")

def _generate_registration_jwt(user_id: int) -> str:
    return _generate_jwt_token({
        "type": "register",
        "user_id": user_id,
        'exp': time() + 600
    })

def _check_registration_jwt(token: str) -> dict:
    data = _check_jwt_token(token)

    if data.get('type') != 'register':
        raise AuthJWTTokenInvalidException("JWT token has wrong type.")

    return data

def _generate_recovery_jwt(user_id: int) -> str:
    return _generate_jwt_token({
        "type": "recovery",
        "user_id": user_id,
        'exp': time() + 600
    })

def _check_recovery_jwt(token: str) -> dict:
    data = _check_jwt_token(token)

    if data.get('type') != 'recovery':
        raise AuthJWTTokenInvalidException("JWT token has wrong type.")

    return data

def _create_access_token(user: User) -> str:
    return create_access_token(user.id)

def _create_refresh_token(user: User) -> str:
    return create_refresh_token(user.id)

def generate_auth_tokens(user: User) -> [str, str]:
    return _create_access_token(user), _create_refresh_token(user)

class AuthService:
    
    def __init__(self, user_service: UserService, email_service: EmailService):
        self.user_service = user_service
        self.email_service = email_service

    def register_user(self, email, password) -> None:
        password_hash = generate_password_hash(password)

        try:
            user = User(
                id=None,
                email=email,
                password=password_hash,
            )

            user = self.user_service.create_user(user)

            self.send_verification_email(user)
        except UserEmailAlreadyTakenException as e:
            raise AuthEmailAlreadyTakenException(e.args[0])


    def login_user(self, email: str, password: str) -> [str, str]:
        try:
            user = self.user_service.get_by_email(email)

            if check_password_hash(user.password, password):
                return generate_auth_tokens(user)
            else:
                raise AuthPasswordNotMatchException("Incorrect password.")
        except UserNotFoundException:
            raise AuthUserWithLoginNotExistException("User with this email does not exist.")


    def send_verification_email(self, user: User) -> None:
        jwt_token = _generate_registration_jwt(user.id)

        self.email_service.send_email(
            "Подтверждение почты",
            recipients=[user.email],
            text=render_template("email/approve_email.txt", token=jwt_token),
            html=render_template("email/approve_email.html", token=jwt_token)
        )


    def verify_user_registration(self, token: str) -> [str, str]:
        user_id = _check_registration_jwt(token)["user_id"]

        if user_id is None:
            raise AuthJWTTokenExpiredException("Verification token is expired.")

        try:
            user = self.user_service.get_by_id(user_id)

            user = self.user_service.update_user(user, {"is_verified": True})

            return generate_auth_tokens(user)
        except UserNotFoundException:
            raise AuthJWTTokenInvalidException("User with this id does not exist.")


    def send_recovery_message(self, email: str) -> None:
        try:
            user = self.user_service.get_by_email(email)

            recovery_token = _generate_recovery_jwt(user.id)

            self.email_service.send_email(
                "Восстановление пароля",
                recipients=[email],
                text=render_template("email/recovery_password.txt", token=recovery_token),
                html=render_template("email/recovery_password.html", token=recovery_token)
            )
        except UserNotFoundException:
            raise AuthUserWithEmailNotExistException("User with this email does not exist.")


    def update_password(self, token: str, old_password: str, new_password: str) -> None:
        try:
            data = _check_recovery_jwt(token)

            user = self.user_service.get_by_id(data["user_id"])

            if not check_password_hash(user.password, old_password):
                raise AuthPasswordNotMatchException("Incorrect password.")

            new_password_hash = generate_password_hash(new_password)

            self.user_service.update_user(user, {"password": new_password_hash})
        except KeyError:
            raise AuthJWTTokenExpiredException("Can't parse user id.")
        
    
    def recovery_password(self, token: str, new_password: str) -> None:
        try:
            data = _check_recovery_jwt(token)

            user = self.user_service.get_by_id(data["user_id"])

            new_password_hash = generate_password_hash(new_password)

            UserService.update_user(user, {"password": new_password_hash})
        except KeyError:
            raise AuthJWTTokenExpiredException("Can't parse user id.")