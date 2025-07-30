from typing import Optional, List

from datetime import datetime

from sqlalchemy import ForeignKey, Text, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.databases import sqlalchemy_db as db
from app.infrastructure.models.sql_base import SQLBaseModel
from app.infrastructure.models.manga.sql_manga_type import SQLMangaType

class SQLManga(db.Model, SQLBaseModel):
    __tablename__ = 'manga'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("manga_type.id"), nullable=True)
    status_id: Mapped[Optional[int]] = mapped_column(ForeignKey("manga_status.id"), nullable=True)
    main_poster_number: Mapped[Optional[int]] = mapped_column(nullable=True)
    background: Mapped[str] = mapped_column(nullable=True)
    year: Mapped[Optional[int]] = mapped_column(nullable=True)
    views: Mapped[Optional[int]] = mapped_column(default=0)
    adult_id: Mapped[Optional[int]] = mapped_column(ForeignKey("manga_adult.id"), nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.utcnow(), nullable=True)
    verified: Mapped[bool] = mapped_column(default=False)


    name_translations: Mapped[List["SQLMangaNameTranslation"]] = relationship()
    type: Mapped["SQLMangaType"] = relationship()
    status: Mapped["SQLMangaStatus"] = relationship()
    main_poster: Mapped["SQLPoster"] = relationship(
        primaryjoin="and_(SQLPoster.order == SQLManga.main_poster_number, SQLPoster.manga_id == SQLManga.id)",
        uselist=False
    )
    posters: Mapped[List["SQLPoster"]] = relationship(uselist=True, back_populates="manga")
    adult: Mapped["SQLMangaAdult"] = relationship()
    genres: Mapped[List["SQLMangaGenre"]] = relationship("Genre", secondary="manga_genre")
    authors: Mapped[List["SQLUser"]] = relationship(secondary="manga_author", uselist=True)
    artists: Mapped[List["SQLUser"]] = relationship(secondary="manga_artist", uselist=True)
    publishers: Mapped[List["SQLUser"]] = relationship(secondary="manga_publisher", uselist=True)
    creator: Mapped["SQLUser"] = relationship()
    translations: Mapped[List["SQLMangaTranslation"]] = relationship("Translation", uselist=True, back_populates="manga")