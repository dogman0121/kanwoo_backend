from flask import render_template, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_csrf_token
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


class JWTService:
    def __init__(self, secret_key, algorithm):
        self.secret_key = secret_key.encode()
        self.algorithm = algorithm

    def encode_jwt(self, payload):
        return jwt.encode(
            payload=payload,
            key=self.secret_key,
            algorithm = self.algorithm
        )
    
    def decode_jwt(self, token):
        try:
            data = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            return data
        except jwt.ExpiredSignatureError:
            raise AuthJWTTokenExpiredException("JWT token is expired.")
        except jwt.InvalidTokenError:
            raise AuthJWTTokenInvalidException("JWT token is invalid.")
        except Exception as e:
            raise AuthJWTTokenInvalidException("JWT token is invalid.")
        
    def create_access_token(self, user_id):
        return create_access_token(str(user_id))

    def create_refresh_token(self, user_id):
        return create_refresh_token(str(user_id))

    def get_csrf_token(self, token):
        return get_csrf_token(token)

    def create_auth_tokens(self, user_id):
        return self.create_access_token(user_id), self.create_refresh_token(user_id)



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
        jwt_service: JWTService,
        hash_service: HashService,
        verification_code_service: VerificationCodeService,
        frontend_url: str
    ):
        self.user_service = user_service
        self.email_service = email_service
        self.jwt_service = jwt_service
        self.hash_service = hash_service
        self.verification_code_service = verification_code_service
        self.frontend_url = frontend_url

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

            token = self.jwt_service.encode_jwt({"user_id": user.id, "exp": time.time() + 600})

            self.email_service.send_email(
                "Восстановление пароля",
                recipients=[email],
                text=render_template("email/recovery_password.txt", base_url=self.frontend_url, token=token),
                html=render_template("email/recovery_password.html", base_url=self.frontend_url, token=token)
            )
        except UserNotFoundException:
            raise AuthUserWithEmailNotExistException("User with this email does not exist.")
    
    
    def system_recovery_password(self, recovery_dto: AuthRecoveryDTO) -> None:
        try:
            token = recovery_dto.token
            new_password = recovery_dto.new_password

            data = self.jwt_service.decode_jwt(token)

            user_id = data.get("user_id")
            
            user = self.user_service.system_get_user_by_id(user_id)

            new_password_hash = self.hash_service.generate_password_hash(new_password)

            self.user_service.system_update_user(user, {"password": new_password_hash})
        except VerificationCodeExpiredException:
            raise AuthVerificationCodeExpiredException