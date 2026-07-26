from dependency_injector import containers, providers

from .repositories import NotificationRepository
from .services import NotificationService
from .permissions import NotificationPolicy

class NotificationContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    db_transaction = providers.Dependency()

    notification_repo = providers.Singleton(
        NotificationRepository,
        db_session=db_session
    )

    notification_policy = providers.Factory(
        NotificationPolicy
    )

    notification_service = providers.Factory(
        NotificationService,
        db_transaction=db_transaction,
        notification_policy=notification_policy,
        notification_repo=notification_repo
    )



    