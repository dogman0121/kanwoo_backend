from dependency_injector import containers, providers

from .repositories import ReadingHistoryRepository, ReadingBookmarkRepository, ReadingSessionRepository
from .services import (
    ReadingHistoryService, 
    ReadingBookmarkService,
    ReadingBookmarkContextService, 
    ReadingSessionService, 
    ChapterProgressService,
    MangaReadingStartService
)

class ReadingProgressContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    db_transaction = providers.Dependency()

    manga_translation_service = providers.Dependency()

    reading_history_repo = providers.Singleton(
        ReadingHistoryRepository,
        db_session=db_session
    )

    reading_bookmark_repo = providers.Singleton(
        ReadingBookmarkRepository,
        db_session=db_session
    )

    reading_session_repo = providers.Singleton(
        ReadingSessionRepository,
        db_session=db_session
    )

    reading_bookmark_service = providers.Factory(
        ReadingBookmarkService,
        reading_bookmark_repo=reading_bookmark_repo,
        db_transaction=db_transaction
    )

    reading_bookmark_context_service = providers.Factory(
        ReadingBookmarkContextService
    )

    reading_history_service = providers.Factory(
        ReadingHistoryService,
        reading_bookmark_service=reading_bookmark_service,
        reading_history_repo=reading_history_repo,
        db_transaction=db_transaction
    )

    reading_session_service = providers.Factory(
        ReadingSessionService,
        reading_session_repo=reading_session_repo,
        reading_history_service=reading_history_service,
        db_transaction=db_transaction
    )

    chapter_progress_service = providers.Factory(
        ChapterProgressService,
        reading_history_repo=reading_history_repo
    )

    manga_reading_start_service = providers.Factory(
        MangaReadingStartService,
        reading_bookmark_repo=reading_bookmark_repo,
        manga_translation_service=manga_translation_service
    )