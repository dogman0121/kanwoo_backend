from dependency_injector import containers, providers

from .repositories import CollectionRepository
from .services import CollectionService
from .permissions import CollectionPolicy

class CollectionContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    manga_repo = providers.Dependency()

    collection_repo = providers.Singleton(
        CollectionRepository,
        db_session=db_session
    )

    collection_policy = providers.Singleton(
        CollectionPolicy
    )

    db_transaction = providers.Dependency()

    collection_service = providers.Factory(
        CollectionService,
        collection_repo=collection_repo,
        db_transaction=db_transaction,
        collection_policy=collection_policy,
        manga_repo=manga_repo
    )