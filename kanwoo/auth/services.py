from flask import render_template, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
import random
import jwt
import time

from kanwoo.cache import Cache
from kanwoo.email import EmailService
from kanwoo.user.exceptions import UserEmailAlreadyTakenException, UserNotFoundException
from kanwoo.user.models import User
from kanwoo.user.dto import UserCreateDTO
from kanwoo.user.services import UserService

from .exceptions import AuthEmailAlreadyTakenException, \
    AuthUserWithLoginNotExistException, AuthPasswordNotMatchException, \
    AuthUserWithEmailNotExistException, AuthJWTTokenInvalidException, AuthJWTTokenExpiredException, \
    VerificationCodeExpiredException, AuthVerificationCodeExpiredException, AuthWrongVerificationCodeException
from .dto import AuthRegisterDTO, AuthRecoveryDTO, AuthLoginDTO

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

def _create_access_token(user: User) -> str:
    return create_access_token(user.id)

def _create_refresh_token(user: User) -> str:
    return create_refresh_token(user.id)

def generate_auth_tokens(user: User):
    return _create_access_token(user), _create_refresh_token(user)

class HashService:
    def __init__(self, method="scrypt", salt_length = 16):
        self.method = method
        self.salt_length = salt_length

    def generate_password_hash(self, password):
        return generate_password_hash(password, method=self.method, salt_length=self.salt_length)
    
    def check_password_hash(self, password_hash, password):
        return check_password_hash(password_hash, password)
    

class VerificationCodeService:
    CODE_EXPIRES_TIME = 300 # seconds

    def __init__(self, cache: Cache):
        self.cache = cache

    def _generate_code(self):
        return str(random.randint(100000, 999999))
    
    def _get_email_verification_key(self, email):
        return f"auth:verification:code:{email}"

    def _get_recovery_key(self, email):
        return f"auth:recovery:code:{email}"

    def get_email_verification_code(self, email):
        code = self._generate_code()

        self.cache.set(self._get_email_verification_key(email), str(code), self.CODE_EXPIRES_TIME)

        return code

    def get_recovery_code(self, email):
        code = self._generate_code()

        self.cache.set(self._get_recovery_key(email), code, self.CODE_EXPIRES_TIME)

        return code

    def check_email_verification_code(self, email, code):
        code_from_cache = self.cache.get(self._get_email_verification_key(email))

        if code_from_cache is None:
            raise VerificationCodeExpiredException(f"Verification code for email {email} is expired.")
        
        return code_from_cache == str(code)

    def check_recovery_code(self, email, code):
        code_from_cache = self.cache.get(self._get_recovery_key(email))

        if code_from_cache is None:
            raise VerificationCodeExpiredException(f"Verification code for email {email} is expired.")
        
        return code_from_cache == str(code)


class AuthService:
    
    def __init__(
        self, 
        user_service: UserService, 
        email_service: EmailService,
        hash_service: HashService,
        verification_code_service: VerificationCodeService
    ):
        self.user_service = user_service
        self.email_service = email_service
        self.hash_service = hash_service
        self.verification_code_service = verification_code_service

    def system_register_user(self, register_dto: AuthRegisterDTO) -> User:
        code = register_dto.code
        email = register_dto.email
        password = register_dto.password

        try: 
            if not self.verification_code_service.check_email_verification_code(email, code):
                raise AuthWrongVerificationCodeException(error="invalid_code", detail={"code": ["Invalid code"]})
            
            password_hash = self.hash_service.generate_password_hash(password)

            user_create_dto = UserCreateDTO(
                email=email,
                password_hash=password_hash
            )

            return self.user_service.system_create_user(user_create_dto)
        except VerificationCodeExpiredException:
            raise AuthVerificationCodeExpiredException
        except UserEmailAlreadyTakenException:
            raise AuthEmailAlreadyTakenException(error="email_exists", detail={"email": ["User with email already exists"]})

    def system_login_user(self, login_dto: AuthLoginDTO):
        email = login_dto.email
        password = login_dto.password

        try:
            user = self.user_service.system_get_user_by_email(email)

            if self.hash_service.check_password_hash(user.password, password):
                return user
            else:
                raise AuthPasswordNotMatchException(error="invalid_credentials", detail={"password": ["Invalid credentials"]})
        except UserNotFoundException:
            raise AuthUserWithLoginNotExistException("User with this email does not exist.")


    def system_send_email_verification_message(self, email) -> None:
        try:
            self.user_service.system_get_user_by_email(email)

            raise AuthEmailAlreadyTakenException(error="email_exists", detail={"email": ["User with email already exists"]})
        except UserNotFoundException:
            pass

        code = self.verification_code_service.get_email_verification_code(email)

        self.email_service.send_email(
            "Подтверждение регистрации",
            recipients=[email],
            text=render_template("email/verify_email.txt", code=code),
            html=render_template("email/verify_email.html", code=code)
        )

    def system_send_recovery_message(self, email: str) -> None:
        try:
            user = self.user_service.system_get_user_by_email(email)

            token = _generate_jwt_token({"user_id": user.id, "exp": time.time() + 600})
            base_url = current_app.config.get("FRONTEND_URI")

            self.email_service.send_email(
                "Восстановление пароля",
                recipients=[email],
                text=render_template("email/recovery_password.txt", base_url=base_url, token=token),
                html=render_template("email/recovery_password.html", base_url=base_url, token=token)
            )
        except UserNotFoundException:
            raise AuthUserWithEmailNotExistException("User with this email does not exist.")
    
    
    def system_recovery_password(self, recovery_dto: AuthRecoveryDTO) -> None:
        try:
            token = recovery_dto.token
            new_password = recovery_dto.new_password

            data = _check_jwt_token(token)

            user_id = data.get("user_id")
            
            user = self.user_service.system_get_user_by_id(user_id)

            new_password_hash = self.hash_service.generate_password_hash(new_password)

            self.user_service.system_update_user(user, {"password": new_password_hash})
        except VerificationCodeExpiredException:
            raise AuthVerificationCodeExpiredException