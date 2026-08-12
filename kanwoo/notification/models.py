from PIL.ImageChops import offset
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from kanwoo.models import Base


class NotificationSettings(Base):
    __tablename__ = "notifications_settings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    new_subscriptions: Mapped[bool] = mapped_column(default=True)
    new_chapters: Mapped[bool] = mapped_column(default=True)
    new_chapters_telegram: Mapped[bool] = mapped_column(default=False) 
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))

    profile: Mapped["Profile"] = relationship()

class NotificationType(Base):
    __tablename__ = "notification_type"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()


class Notification(Base):
    __tablename__ = "notification"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey('profile.id'), nullable=False)
    action: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    chapter_id: Mapped[int] = mapped_column(ForeignKey('chapter.id'), nullable=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey('profile.id'), nullable=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey('comment.id'), nullable=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey('manga.id'), nullable=True)
    is_read: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    profile: Mapped["Profile"] = relationship(foreign_keys=[profile_id])
    chapter: Mapped["Chapter"] = relationship()
    actor: Mapped["Profile"] = relationship(foreign_keys=[actor_id])
    comment: Mapped["Comment"] = relationship()
    manga: Mapped["Manga"] = relationship()
