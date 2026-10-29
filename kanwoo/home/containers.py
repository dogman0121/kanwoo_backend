from dependency_injector import providers, containers

from .repositories import HomeRepository
from .services import HomeService

class HomeContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    reading_progress_service = providers.Dependency()
    chapter_service = providers.Dependency()
    manga_stats_service = providers.Dependency()

    home_service = providers.Factory(
        HomeService,
        chapter_service=chapter_service,
        manga_stats_service=manga_stats_service,
        reading_progress_service=reading_progress_service
    )