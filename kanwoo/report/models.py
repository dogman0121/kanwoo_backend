from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from datetime import datetime

from kanwoo.models import Base

class ReportType(Base):
    __tablename__ = "report_type"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column()

class Report(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("report_type.id"))
    comment: Mapped[str] = mapped_column()
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.now())
    resolved_at: Mapped[datetime] = mapped_column(nullable=True)
    resolver_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
 
    @declared_attr
    def creator(cls):
        return relationship("Profile", foreign_keys=[cls.creator_id], uselist=False)
    
    @declared_attr
    def resolver(cls):
        return relationship("Profile", foreign_keys=[cls.resolver_id], uselist=False)

class MangaReport(Report):
    __tablename__ = "manga_report"

    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"))

    manga: Mapped["Manga"] = relationship()

class ChapterReport(Report):
    __tablename__ = "chapter_report"

    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))

    chapter: Mapped["Chapter"] = relationship()