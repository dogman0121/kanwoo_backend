from dependency_injector import containers, providers

from .repositories import CommentRepository
from .services import CommentService
from .permissions import CommentPolicy

class CommentContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    db_transaction = providers.Dependency()

    comment_repo = providers.Singleton(
        CommentRepository,
        db_session=db_session
    )

    comment_policy = providers.Factory(
        CommentPolicy
    )

    comment_service = providers.Factory(
        CommentService,
        db_transaction=db_transaction,
        comment_policy=comment_policy,
        comment_repo=comment_repo
    )



    