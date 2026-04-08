from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from kanwoo.models import Base

class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"), primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), primary_key=True)
    page: Mapped[int] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.now(), nullable=True)

    chapter: Mapped["Chapter"] = relationship()
    profile: Mapped["Profile"] = relationship()
    
    @hybrid_property
    def manga(self):
        return self.chapter.translation.manga