from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.models import Base


class Translation(Base):
    __tablename__ = "translation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.utcnow(), nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)

    chapters: Mapped[list["Chapter"]] = relationship(uselist=True, lazy="dynamic", back_populates="translation")
    creator: Mapped["Profile"] = relationship("Profile")
    manga: Mapped["Manga"] = relationship("Manga", back_populates="translations")

    @hybrid_property
    def chapters_count(self):
        return self.chapters.count()