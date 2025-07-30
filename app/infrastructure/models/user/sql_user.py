from datetime import datetime

from sqlalchemy import String, Integer, Text, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.infrastructure.databases import sqlalchemy_db as db
from app.infrastructure.models.sql_base import SQLBaseModel

class SQLUser(db.Model, SQLBaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password: Mapped[str] = db.Column(Text, nullable=False)
    role: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    avatar: Mapped["SQLAvatar"] = relationship()
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user", uselist=True,
                                                               foreign_keys="Notification.user_id")
    lists: Mapped[list["List"]] = relationship(back_populates="creator", foreign_keys="List.creator_id", uselist=True)
