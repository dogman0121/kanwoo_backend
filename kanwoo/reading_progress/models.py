from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, select
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from kanwoo.models import Base
from kanwoo.chapter.models import Chapter

class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"), nullable=True)
    translation_id: Mapped[int] = mapped_column(ForeignKey("translation.id"), nullable=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    page: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.now(), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(nullable=True, default=False)

    chapter: Mapped["Chapter"] = relationship()
    profile: Mapped["Profile"] = relationship()
    manga: Mapped["Manga"] = relationship(viewonly=True)
    translation: Mapped["Translation"] = relationship()
    
    @hybrid_property
    def chapters_count(self):
        return self.translation.chapters_count
    
    @chapters_count.expression
    def chapters_count(self):
        return select(func.count(Chapter.id)).where(Chapter.id == self.chapter_id)