from flask import current_app

from app import db, storage
from app.models import Base

from sqlalchemy import (Table, ForeignKey, Column, String, Integer,
                        DateTime, Text, insert, delete, select, and_, func,
                        Select, Boolean)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time

oauth = Table(
    'oauth',
    db.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False),
    Column("oauth_type", String(20), nullable=False),
    Column("oauth_id", Text, nullable=False),
)

user_subscribers = Table(
    'user_subscriber',
    db.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False, primary_key=True),
    Column("subscriber_id", Integer, ForeignKey("user.id"), nullable=False, primary_key=True),
)

class Avatar(Base):
    __tablename__ = "avatar"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(64), nullable=False)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    password: Mapped[str] = db.Column(Text, nullable=False)
    role: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    avatar_obj: Mapped["Avatar"] = relationship(Avatar)
    lists: Mapped[list["List"]] = relationship(
        back_populates="creator",
        foreign_keys="List.creator_id",
        uselist=True
    )

    @hybrid_property
    def subscribers_count(self):
        return db.session.execute(select(func.count(user_subscribers.c.user_id))
            .where(self.id == user_subscribers.c.user_id)
        ).scalar()

    @hybrid_property
    def avatar(self):
        if self.avatar_obj:
            return storage.get_url(f"user/{self.id}/{self.avatar_obj.filename}")
        else:
            return ""