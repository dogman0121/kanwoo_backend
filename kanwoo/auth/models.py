from sqlalchemy import Table, Column, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from kanwoo.models import Base



class Oauth(Base):
    __tablename__ = 'oauth'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    oauth_type_id: Mapped[int] = mapped_column(ForeignKey("oauth_type.id"))
    oauth_user_id: Mapped[str] = mapped_column()

    user: Mapped["User"] = relationship("User")


class OauthType(Base):
    __tablename__ = "oauth_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()