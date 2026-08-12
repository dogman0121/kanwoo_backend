from dependency_injector import containers, providers

from .repositories import PostRepository
from .services import PostService
from .permissions import PostPolicy

class PostContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    db_transaction = providers.Dependency()

    post_repo = providers.Singleton(
        PostRepository,
        db_session=db_session
    )

    post_policy = providers.Factory(
        PostPolicy
    )

    post_service = providers.Factory(
        PostService,
        db_transaction=db_transaction,
        notification_policy=post_policy,
        notification_repo=post_repo
    )



    