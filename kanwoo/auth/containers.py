from dependency_injector import containers, providers

from .services import AuthService, HashService, VerificationCodeService, JWTService, YandexOauthService
from .repositories import AuthRepository

class AuthContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    cache = providers.Dependency()

    db_session = providers.Dependency()

    email_service = providers.Dependency()

    user_service = providers.Dependency()

    user_repo = providers.Dependency()

    db_transaction = providers.Dependency()

    auth_repo = providers.Singleton(
        AuthRepository,
        db_session=db_session
    )

    jwt_service = providers.Factory(
        JWTService,
        secret_key=config.SECRET_KEY,
        algorithm="HS256"
    )

    yandex_oauth_service = providers.Factory(
        YandexOauthService,
        client_secret=config.YANDEX_OAUTH_SECRET_KEY,
        oauth_login_url=config.YANDEX_OAUTH_LOGIN_URL,
        avatars_url=config.YANDEX_AVATARS_URL,
        avatars_size=config.YANDEX_AVATARS_SIZE
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
        frontend_url=config.FRONTEND_URL,
        yandex_oauth_service=yandex_oauth_service,
        db_transaction=db_transaction,
        user_repo=user_repo,
        auth_repo=auth_repo
    )