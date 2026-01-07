from PIL.ImageChops import offset
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app import db
from app.models import Base


class NotificationService:
    page_size = 10

    @staticmethod
    def get_user_notifications(user, page=1):
        return Notification.query.filter_by(user_id=user.id).limit(NotificationService.page_size).offset(
            (page - 1) * NotificationService.page_size).all()

    @staticmethod
    def get_all_user_notification_count(user):
        return Notification.query.filter_by(user_id=user.id).count()

    @staticmethod
    def get_unread_user_notifications_count(user):
        return Notification.query.filter_by(user_id=user.id, is_read=False).count()

    @staticmethod
    def get_unread_user_notifications(user):
        return Notification.query.filter_by(user_id=user.id, is_read=False).all()

    @staticmethod
    def read_all_user_notifications(user):
        notifications = NotificationService.get_user_notifications(user)
        for notification in notifications:
            notification.is_read = True
        db.session.commit()

class Notification(Base):
    __tablename__ = "notification"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey('profile.id'), nullable=False)
    action: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=True)
    # post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    chapter_id: Mapped[int] = mapped_column(ForeignKey('chapter.id'), nullable=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey('profile.id'), nullable=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey('comment.id'), nullable=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey('manga.id'), nullable=True)
    is_read: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    profile: Mapped["Profile"] = relationship(foreign_keys=[profile_id])
    chapter: Mapped["Chapter"] = relationship()
    actor: Mapped["Profile"] = relationship(foreign_keys=[actor_id])
    comment: Mapped["Comment"] = relationship()
    manga: Mapped["Manga"] = relationship()

    def read(self):
        self.is_read = True
        self.update()

    def _render_payload(self):
        payload = {}
        if self.profile_id:
            payload["profile"] = self.actor.to_dict()

        if self.team_id:
            return {}

        if self.comment_id:
            payload["comment"] = self.comment.to_dict()

        if self.manga_id:
            return {}

        if self.chapter_id:
            payload["chapter"] = self.chapter.to_dict()

        return payload