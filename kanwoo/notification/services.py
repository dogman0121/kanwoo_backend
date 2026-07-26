from kanwoo.database import DBTransaction

from .repositories import NotificationRepository
from .permissions import NotificationPolicy


class NotificationService:

    def __init__(
        self,
        notification_repo: NotificationRepository,
        notification_policy: NotificationPolicy,
        db_transaction: DBTransaction
    ):
        self.notification_repo = notification_repo
        self.notification_policy = notification_policy
        self.db_trasaction = db_transaction