from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.infrastructure.databases import sqlalchemy_db as db
from app.infrastructure.models.sql_base import SQLBaseModel

class SQLMangaTranslation(db.Model, SQLBaseModel):
    __tablename__ = "manga_translation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)

    chapters: Mapped[list["Chapter"]] = relationship(uselist=True, lazy="dynamic", back_populates="translation")
    team: Mapped["Team"] = relationship("Team")
    user: Mapped["User"] = relationship("User")
    manga: Mapped["SQLManga"] = relationship("Manga", back_populates="translations")