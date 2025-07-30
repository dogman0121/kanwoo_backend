from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.models.sql_base import SQLBaseModel
from app.infrastructure.databases.sql_alchemy import sqlalchemy_db as db

from datetime import datetime


class SQLFile(db.Model, SQLBaseModel):
    __abstract__ = True

    uuid: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    uploaded_at: Mapped[datetime] = mapped_column(nullable=False, default=lambda x: datetime.now())