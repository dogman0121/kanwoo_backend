from datetime import datetime

from kanwoo.models import Base

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

class ModerationStatusType(Base):
    __tablename__ = "moderation_status_type"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()


class ModerationStatus(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    status_type_id: Mapped[int] = mapped_column(ForeignKey("moderation_status_type.id"))
    message: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.utcnow())
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)

    @declared_attr
    def creator(cls):
        return relationship("Profile", uselist=False)
    
    @declared_attr
    def status_type(cls):
        return relationship("ModerationStatusType", uselist=False)

class MangaModerationStatus(ModerationStatus):
    __tablename__ = "manga_moderation_status"

    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"))


class ChapterModerationStatus(ModerationStatus):
    __tablename__ = "chapter_moderation_status"

    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))