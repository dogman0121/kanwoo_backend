from dependency_injector import containers, providers

from .repositories import ReadingProgressRepository, ReadingSaveRepository
from .services import ReadingProgressService

class ReadingProgressContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    db_transaction = providers.Dependency()

    reading_progress_repo = providers.Singleton(
        ReadingProgressRepository,
        db_session=db_session
    )

    reading_save_repo = providers.Singleton(
        ReadingSaveRepository,
        db_session=db_session
    )

    reading_progress_service = providers.Factory(
        ReadingProgressService,
        progress_repo=reading_progress_repo,
        save_repo=reading_save_repo,
        db_transaction=db_transaction
    )