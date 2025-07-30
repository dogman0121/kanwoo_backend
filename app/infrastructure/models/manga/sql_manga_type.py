from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.databases import sqlalchemy_db as db
from app.infrastructure.models.sql_base import SQLBaseModel

class SQLMangaType(db.Model, SQLBaseModel):
    __tablename__ = "manga_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)