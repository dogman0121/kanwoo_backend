from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from kanwoo.models import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    message: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.now())
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
    resolved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    resolver_id: Mapped[datetime] = mapped_column(ForeignKey("profile.id"), nullable=True)

    creator: Mapped["Profile"] = relationship(foreign_keys=[creator_id])
    resolver: Mapped["Profile"] = relationship(foreign_keys=[resolver_id])