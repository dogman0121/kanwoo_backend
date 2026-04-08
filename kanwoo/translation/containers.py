from dependency_injector import containers, providers

from .repositories import TranslationRepository
from .services import TranslationService
from .services import TranslationPolicy

class TranslationContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    translation_repo = providers.Singleton(
        TranslationRepository,
        db_session=db_session
    )

    translation_policy = providers.Singleton(
        TranslationPolicy
    )

    translation_service = providers.Factory(
        TranslationService,
        translation_repo=translation_repo,
        translation_policy=translation_policy
    )