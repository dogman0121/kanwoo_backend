from dependency_injector import providers, containers

from .repositories import ChapterRepository
from .services import ChapterPageService, ChapterService
from .permissions import ChapterPolicy


class ChapterContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    image_service_factory = providers.Dependency()

    storage = providers.Dependency()

    chapter_repo = providers.Singleton(
        ChapterRepository,
        db_session
    )

    chapter_policy = providers.Singleton(
        ChapterPolicy
    )

    chapter_page_service = providers.Factory(
        ChapterPageService,
        image_service_factory=image_service_factory,
        storage=storage,
        chapter_repo=chapter_repo
    )

    chapter_service = providers.Factory(
        ChapterService,
        chapter_page_service=chapter_page_service,
        chapter_repo=chapter_repo,
        chapter_policy=chapter_policy
    )