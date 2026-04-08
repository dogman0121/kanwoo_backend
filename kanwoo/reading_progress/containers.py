from dependency_injector import containers, providers

from .repositories import ReadingProgressRepository
from .services import ReadingProgressService

class ReadingProgressContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    reading_progress_repo = providers.Singleton(
        ReadingProgressRepository,
        db_session=db_session
    )

    reading_progress_service = providers.Factory(
        ReadingProgressService,
        reading_progress_repo=reading_progress_repo
    )