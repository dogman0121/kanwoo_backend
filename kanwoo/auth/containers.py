from dependency_injector import containers, providers

from .services import AuthService, HashService

class AuthContainer(containers.DeclarativeContainer):

    email_service = providers.Dependency()

    hash_service = providers.Factory(
        HashService,
        method="scrypt",
        salt_length=16
    )

    user_service = providers.Dependency()

    auth_service = providers.Factory(
        AuthService,
        email_service=email_service,
        user_service=user_service,
        hash_service=hash_service
    )