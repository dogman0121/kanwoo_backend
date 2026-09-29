from dependency_injector import providers, containers

from .repositories import HomeRepository
from .services import HomeService

class HomeContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    reading_progress_service = providers.Dependency()

    home_repo = providers.Singleton(
        HomeRepository, 
        db_session=db_session
    )

    home_service = providers.Factory(
        HomeService,
        home_repo=home_repo,
        reading_progress_service=reading_progress_service
    )