from typing import List

from kanwoo.database import DBTransaction
from kanwoo.profile.models import Profile

from .repositories import NotificationRepository
from .permissions import NotificationPolicy
from .entity import NotificationDeleteModeEnum
from .exceptions import NotificationDeleteNotAllowed


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

    def user_get_notifications(self, profile, page, per_page):
        return self.notification_repo.get_profile_notifications(profile, page, per_page)


    def user_delete_notifications(self, profile: Profile, mode: NotificationDeleteModeEnum, notifications_ids: List[int] = []):
        if mode == NotificationDeleteModeEnum.ALL:
            self.notification_repo.delete_all_profile_notifications(profile)
        if mode == NotificationDeleteModeEnum.SELECTED:
            if self.notification_repo.check_notifications_recipient(profile, notifications_ids):
                self.notification_repo.delete_selected_profile_notifications(profile, notifications_ids)
            else:
                raise NotificationDeleteNotAllowed()

    def user_read_notifications(self, profile: Profile):
        return self.notification_repo.read_notifications(profile)


    def system_send_user_subscribe_notification():
        pass

    def system_send_comment_reply_notification():
        pass

    def system_send_new_chapter_notification():
        pass