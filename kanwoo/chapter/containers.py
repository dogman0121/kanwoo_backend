from dependency_injector import providers, containers

from .repositories import ChapterRepository
from .services import (
    ChapterPageService, 
    ChapterService,
    ChapterContextService,
    ChapterPublicService,
    ChapterFrontendMetadataService
)
from .permissions import ChapterPolicy


class ChapterContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    db_transaction = providers.Dependency()

    image_service_factory = providers.Dependency()

    file_storage = providers.Dependency()

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
        file_storage=file_storage,
        chapter_repo=chapter_repo
    )

    chapter_service = providers.Factory(
        ChapterService,
        chapter_page_service=chapter_page_service,
        chapter_repo=chapter_repo,
        chapter_policy=chapter_policy,
        db_transaction=db_transaction
    )

    chapter_public_service = providers.Factory(
        ChapterPublicService,
        chapter_repo=chapter_repo
    )

    chapter_frontend_metadata_service = providers.Factory(
        ChapterFrontendMetadataService,
        chapter_public_service=chapter_public_service
    )

    chapter_context_service = providers.Factory(
        ChapterContextService
    )