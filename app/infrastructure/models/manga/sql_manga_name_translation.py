from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.databases import sqlalchemy_db as db
from app.infrastructure.models.sql_base import SQLBaseModel

class SQLMangaNameTranslation(db.Model, SQLBaseModel):
    __tablename__ = "manga_name_translation"

    manga_id: Mapped[int] = mapped_column(Integer, ForeignKey("manga.id"), primary_key=True,
                                          nullable=False)
    lang: Mapped[str] = mapped_column(String(5), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)