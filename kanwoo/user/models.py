from kanwoo import db
from kanwoo.models import Base

from sqlalchemy import (String, Integer,
                        DateTime, Text)
from sqlalchemy.orm import mapped_column, Mapped

from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    password: Mapped[str] = db.Column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)