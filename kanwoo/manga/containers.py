from dependency_injector import containers, providers

from .repositories import MangaRepository, MangaSuggestionRepository
from .services import MangaMediaService, MangaService, MangaSuggestionService
from .permissions import MangaPolicy

class MangaContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    storage = providers.Dependency()

    image_service_factory = providers.Dependency()

    manga_repo = providers.Singleton(
        MangaRepository,
        db_session=db_session
    )

    manga_policy = providers.Singleton(
        MangaPolicy
    )

    manga_media_service = providers.Factory(
        MangaMediaService,
        image_service_factory=image_service_factory,
        manga_repo=manga_repo,
        storage=storage
    )

    manga_service = providers.Factory(
        MangaService,
        manga_media_service=manga_media_service,
        manga_repo=manga_repo,
        manga_policy=manga_policy
    )

    manga_suggestion_repo = providers.Singleton(
        MangaSuggestionRepository,
        db_session=db_session
    )

    manga_suggestion_service = providers.Factory(
        MangaSuggestionService,
        manga_suggestion_repo=manga_suggestion_repo
    )