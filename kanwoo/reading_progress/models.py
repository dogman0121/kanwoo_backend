from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DateTime, func, select, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from kanwoo.models import Base
from kanwoo.chapter.models import Chapter

class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    page: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=True)
    is_finished: Mapped[bool] = mapped_column(nullable=True, default=False)
    is_deleted: Mapped[bool] = mapped_column(nullable=True, default=False)

    chapter: Mapped["Chapter"] = relationship()
    profile: Mapped["Profile"] = relationship()
    
    @hybrid_property
    def chapters_count(self):
        return self.translation.chapters_count
    
    @chapters_count.expression
    def chapters_count(self):
        return select(func.count(Chapter.id)).where(Chapter.id == self.chapter_id)


class ReadingSaveStatus(Base):
    __tablename__ = "reading_save_status_type"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()

class ReadingSave(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"))
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    page: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=True)
    status_type_id: Mapped[int] = mapped_column(ForeignKey("reading_save_status_type.id"))


    chapter: Mapped["Chapter"] = relationship()
    manga: Mapped["Manga"] = relationship()
    profile: Mapped["Profile"] = relationship()

    __table_args__ = (
        UniqueConstraint("manga_id", "profile_id", name="uq_reading_save_progress"),
    )