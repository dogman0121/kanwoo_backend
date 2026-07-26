from kanwoo import db
from kanwoo.models import Base

from sqlalchemy import (
    String, Integer, DateTime, Text
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from datetime import datetime



class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    password: Mapped[str] = db.Column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    yandex_oauth: Mapped["Oauth"] = relationship(
        "Oauth", 
        back_populates="user", 
        primaryjoin="and_(User.id == Oauth.user_id, Oauth.oauth_type_id == 1)"
    )

    @hybrid_property
    def has_password_auth(self):
        return self.password != None

    @hybrid_property
    def has_yandex_oauth(self):
        return self.yandex_oauth != None
