from dependency_injector import containers, providers

from .services import AuthService, HashService, VerificationCodeService, JWTService

class AuthContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    cache = providers.Dependency()

    email_service = providers.Dependency()

    user_service = providers.Dependency()

    jwt_service = providers.Factory(
        JWTService,
        secret_key=config.SECRET_KEY,
        algorithm="HS256"
    )

    hash_service = providers.Factory(
        HashService,
        method="scrypt",
        salt_length=16
    )

    verification_code_service = providers.Factory(
        VerificationCodeService,
        cache=cache
    )

    auth_service = providers.Factory(
        AuthService,
        email_service=email_service,
        user_service=user_service,
        hash_service=hash_service,
        verification_code_service=verification_code_service,
        jwt_service=jwt_service,
        frontend_url=config.FRONTEND_URL
    )