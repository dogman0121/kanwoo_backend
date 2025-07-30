from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.databases import sqlalchemy_db as db
from app.infrastructure.models.sql_base import SQLBaseModel

class SQLMangaGenre(db.Model, SQLBaseModel):
    __tablename__ = "manga_genre"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)