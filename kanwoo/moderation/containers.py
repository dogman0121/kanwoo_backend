from dependency_injector import containers, providers

from .repositories import MangaModerationRepository, ChapterModerationRepository
from .services import ModerationService

class ModertionContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    manga_moderation_repo = providers.Singleton(
        MangaModerationRepository,
        db_session=db_session
    )

    chapter_moderation_repo = providers.Singleton(
        ChapterModerationRepository,
        db_session=db_session
    )

    moderation_service = providers.Factory(
        ModerationService,
        manga_moderation_repo=manga_moderation_repo,
        chapter_moderation_repo=chapter_moderation_repo
    )