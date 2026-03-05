from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from kanwoo.models import Base



class Translation(Base):
    __tablename__ = "translation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=True)
    privacy_id: Mapped[int] = mapped_column(ForeignKey("privacy.id"), nullable=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"))
    lang_id: Mapped[str] = mapped_column(ForeignKey("language.id"), nullable=True)
    is_official: Mapped[bool] = mapped_column(default=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.utcnow(), nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)

    lang: Mapped["Language"] = relationship("Language")
    privacy: Mapped["Privacy"] = relationship("Privacy")
    chapters: Mapped[list["Chapter"]] = relationship(uselist=True, lazy="dynamic", back_populates="translation")
    creator: Mapped["Profile"] = relationship("Profile")
    manga: Mapped["Manga"] = relationship("Manga", back_populates="translations")

    @hybrid_property
    def chapters_count(self):
        return self.chapters.count()