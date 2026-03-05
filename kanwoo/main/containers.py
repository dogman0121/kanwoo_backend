from dependency_injector import providers, containers

from .repositories import MetaRepository, FeedbackRepository
from .services import MetaService, FeedbackService

class MainContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    meta_repo = providers.Singleton(
        MetaRepository,
        db_session=db_session
    )

    meta_service = providers.Factory(
        MetaService,
        meta_repo=meta_repo
    )

    feedback_repo = providers.Singleton(
        FeedbackRepository,
        db_session=db_session
    )

    feedback_service = providers.Factory(
        FeedbackService,
        feedback_repo=feedback_repo
    )