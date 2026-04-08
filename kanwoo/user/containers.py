from dependency_injector import containers, providers

from .repositories import UserRepository
from .services import UserService

class UserContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    user_repo = providers.Singleton(
        UserRepository,
        db_session=db_session
    )

    user_service = providers.Factory(
        UserService,
        user_repo=user_repo
    )