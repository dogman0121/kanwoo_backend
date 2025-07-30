from sqlalchemy import String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.infrastructure.databases import sqlalchemy_db as db
from app.infrastructure.models.sql_base import SQLBaseModel

class SQLMangaPoster(db.Model, SQLBaseModel):
    __tablename__ = "manga_poster"

    id: Mapped[str] = mapped_column(String, primary_key=True, autoincrement=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id", ondelete="CASCADE", onupdate="CASCADE"),
                                          nullable=False)
    orig_filename: Mapped[str] = mapped_column(String, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False)

    manga: Mapped["SQLManga"] = relationship(back_populates="posters")
    files: Mapped[list["PosterFile"]] = relationship(uselist=True, back_populates="poster")