from flask import current_app

from kanwoo import db, file_storage
from kanwoo.models import Base

from sqlalchemy import (Table, ForeignKey, Column, String, Integer,
                        DateTime, Text, Boolean)
from sqlalchemy.orm import mapped_column, Mapped

from datetime import datetime

from time import time

oauth = Table(
    'oauth',
    db.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False),
    Column("oauth_type", String(20), nullable=False),
    Column("oauth_id", Text, nullable=False),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    password: Mapped[str] = db.Column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)