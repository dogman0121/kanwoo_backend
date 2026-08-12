from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from kanwoo import db
from kanwoo.models import Base


class Post(Base):
    __tablename__ = "post"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[int] = mapped_column()
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    created_at: Mapped[datetime] = mapped_column(default=lambda x: datetime.now(timezone.utc))
    is_deleted: Mapped[bool] = mapped_column(default=False)