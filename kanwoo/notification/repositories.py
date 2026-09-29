from sqlalchemy import select, update, func

from kanwoo.models import page_paginate
from kanwoo.repositories import BaseRepository

from .models import Notification

class NotificationRepository(BaseRepository):

    def get_profile_notifications(self, profile, page, per_page):
        query = select(Notification).filter(Notification.recipient_id==profile.id, Notification.is_deleted==False).order_by(Notification.created_at.desc())

        results, total_count = page_paginate(self.db_session, query, page, per_page)

        return results, total_count

    def delete_all_profile_notifications(self, profile):
        self.db_session.execute(
            update(Notification).filter(
                Notification.recipient_id==profile.id).values(Notification.is_deleted==True)
        )

    def check_notifications_recipient(self, profile, notifications_ids):
        results = self.db_session.execute(
            select(
                func.count(Notification))
                .filter(
                    Notification.recipient_id==profile.id, 
                    Notification.id.in_(notifications_ids)
                )
        ).scalar()

        return len(notifications_ids) == results

    def delete_selected_profile_notifications(self, profile, notifications_ids=[]):
        return self.db_session.execute(
            update(Notification)
            .filter(
                Notification.recipient_id==profile.id,
                Notification.id.in_(notifications_ids)
            )
            .values(Notification.is_deleted==True)
        )

    def read_notifications(self, profile):
        return self.db_session.execute(
            update(Notification)
            .filter(
                Notification.recipient_id==profile.id, 
                Notification.is_read==False
            )
            .values(Notification.is_read==True)
        )

    def get_unread_notifications_count(self, profile):
        return self.db_session.execute(
            select(func.count(Notification))
            .filter(Notification.recipient_id==profile.id, Notification.is_read==False)
        ).scalar()