from sqlalchemy import Table, Column, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from kanwoo.models import Base
from kanwoo import db

oauth = Table(
    'oauth',
    db.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False),
    Column("oauth_type_id", Integer, ForeignKey("oauth_type.id"), nullable=False),
    Column("oauth_id", Text, nullable=False),
)

class OauthType(Base):
    __tablename__ = "oauth_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()