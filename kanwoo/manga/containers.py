from dependency_injector import containers, providers

from .repositories import (
    MangaRepository, 
    MangaSuggestionRepository, 
    MangaStatsRepository,
    MangaStatRepository
)
from .services import (
    MangaMediaService, 
    MangaService,
    MangaSuggestionService, 
    MangaStatsService,
    MangaPublicService,
    MangaContextService,
    MangaFrontendMetadataService,
    MangaStatService
)
from .permissions import MangaPolicy

class MangaContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()
    db_transaction = providers.Dependency()
    
    file_storage = providers.Dependency()

    collection_service = providers.Dependency()
    image_service_factory = providers.Dependency()
    moderation_service = providers.Dependency()

    # --- REPO ---
    manga_repo = providers.Singleton(
        MangaRepository,
        db_session=db_session
    )
    manga_stats_repo = providers.Singleton(
        MangaStatsRepository,
        db_session=db_session
    )
    manga_suggestion_repo = providers.Singleton(
        MangaSuggestionRepository,
        db_session=db_session
    )

    manga_policy = providers.Singleton(
        MangaPolicy
    )

    manga_media_service = providers.Factory(
        MangaMediaService,
        image_service_factory=image_service_factory,
        manga_repo=manga_repo,
        file_storage=file_storage
    )

    manga_service = providers.Factory(
        MangaService,
        manga_media_service=manga_media_service,
        manga_repo=manga_repo,
        manga_policy=manga_policy,
        moderation_service=moderation_service,
        collection_service=collection_service,
        db_transaction=db_transaction,
    )

    manga_stats_service = providers.Factory(
        MangaStatsService,
        manga_stats_repo=manga_stats_repo
    )

    manga_suggestion_service = providers.Factory(
        MangaSuggestionService,
        manga_suggestion_repo=manga_suggestion_repo
    )

    manga_public_service = providers.Factory(
        MangaPublicService,
        manga_repo=manga_repo
    )

    manga_frontend_metadata_service = providers.Factory(
        MangaFrontendMetadataService,
        manga_public_service=manga_public_service
    )

    manga_context_service = providers.Factory(
        MangaContextService,
        collection_service=collection_service
    )

    manga_stat_repo = providers.Singleton(
        MangaStatRepository,
        db_session=db_session
    )

    manga_stat_service = providers.Factory(
        MangaStatService,
        manga_stat_repo=manga_stat_repo,
        db_transaction=db_transaction
    )