from dependency_injector import containers, providers

from .services import AuthService

class AuthContainer(containers.DeclarativeContainer):

    email_service = providers.Dependency()

    user_container = providers.Dependency()

    auth_service = providers.Factory(
        AuthService,
        email_service=email_service,
        user_service=user_container.provided.user_service
    )