from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import ForeignKey, DateTime, func, select, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship, column_property
from sqlalchemy.ext.hybrid import hybrid_property

from kanwoo.models import BaseModel
from kanwoo.chapter.models import Chapter


class ReadingHistory(BaseModel):
    __tablename__ = "reading_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))
    reading_session_id: Mapped[int] = mapped_column(ForeignKey("reading_session.id"))
    page: Mapped[int] = mapped_column()
    is_finished: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=True
    )

    chapter: Mapped["Chapter"] = relationship()
    reading_session: Mapped["ReadingSession"] = relationship()


class ReadingSession(BaseModel):
    __tablename__ = "reading_session"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    translation_id: Mapped[int] = mapped_column(ForeignKey("translation.id"))
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=True
    )

    history_items: Mapped[list["ReadingHistory"]] = relationship(
        "ReadingHistory",
        order_by="desc(ReadingHistory.updated_at)",
        lazy="selectin",
        viewonly=True
    )

    profile: Mapped["Profile"] = relationship()
    translation: Mapped["Translation"] = relationship()

    @hybrid_property
    def last_history_item(self) -> Optional["ReadingHistory"]:
        return self.history_items[0] if self.history_items else None

class ReadingBookmark(BaseModel):
    __tablename__ = "reading_bookmark"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"))
    translation_id: Mapped[int] = mapped_column(ForeignKey("translation.id"))
    chapter_number: Mapped[int] = mapped_column()
    page_number: Mapped[int] = mapped_column()
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=True
    )

    manga: Mapped["Manga"] = relationship()
    translation: Mapped["Translation"] = relationship()
    profile: Mapped["Profile"] = relationship()
    chapter: Mapped[Optional["Chapter"]] = relationship(
        primaryjoin="and_(foreign(ReadingBookmark.translation_id) == Chapter.translation_id, foreign(ReadingBookmark.chapter_number) == Chapter.chapter)",
        order_by="Chapter.chapter.asc(), Chapter.extra_number.asc().nulls_first()",
        viewonly=True,
    )

    __table_args__ = (
        UniqueConstraint("manga_id", "profile_id", name="uq_reading_bookmark"),
    )