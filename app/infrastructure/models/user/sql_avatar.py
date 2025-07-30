from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.databases import sqlalchemy_db as db
from app.infrastructure.models.sql_base import SQLBaseModel
from app.infrastructure.models.sql_file import SQLFile


class SQLUserAvatar(db.Model, SQLFile, SQLBaseModel):
    __tablename__ = "user_avatar"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(64), nullable=False)