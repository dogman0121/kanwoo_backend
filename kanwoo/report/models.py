from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from datetime import datetime

from kanwoo.models import Base

class ReportType(Base):
    __tablename__ = "report_type"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column()

class Report(Base):
    __tablename__ = "report"

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

class MangaReport(Base):
    __tablename__ = "manga_report"

    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"), primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("report.id"), primary_key=True)

    manga: Mapped["Manga"] = relationship()
    report: Mapped["Report"] = relationship()

class ChapterReport(Base):
    __tablename__ = "chapter_report"

    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"), primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("report.id"), primary_key=True)

    chapter: Mapped["Chapter"] = relationship()
    report: Mapped["Report"] = relationship()

class CommentReport(Base):
    __tablename__ = "comment_report"

    comment_id: Mapped[int] = mapped_column(ForeignKey("comment.id"), primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("report.id"), primary_key=True)

    comment: Mapped["Comment"] = relationship()
    report: Mapped["Report"] = relationship()
