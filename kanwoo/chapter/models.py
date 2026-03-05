from typing import Optional

from sqlalchemy import ForeignKey, and_, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from kanwoo import storage, db
from kanwoo.models import Base, File

from datetime import datetime

class Page(Base, File):
    __tablename__ = "page"

    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id", ondelete="SET NULL"), nullable=True)
    order: Mapped[int] = mapped_column(nullable=False)


class Chapter(Base):
    __tablename__ = "chapter"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    tome: Mapped[int] = mapped_column(nullable=True)
    chapter: Mapped[int] = mapped_column(nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    translation_id: Mapped[int] = mapped_column(ForeignKey("translation.id"), nullable=True)
    privacy_id: Mapped[int] = mapped_column(ForeignKey("privacy.id"), nullable=True)

    privacy: Mapped["Privacy"] = relationship()
    pages: Mapped[list["Page"]] = relationship(
        primaryjoin="and_(Page.chapter_id==Chapter.id, Page.is_deleted==False)",
        order_by="Page.order"
    )
    translation: Mapped["Translation"] = relationship(back_populates="chapters")
    creator: Mapped["Profile"] = relationship()
    manga: Mapped["Manga"] = relationship("Manga",  primaryjoin="Chapter.translation_id == Translation.id", secondary="translation",
                         secondaryjoin="Translation.manga_id == Manga.id", viewonly=True)

    @hybrid_property
    def next_chapter_id(self):
        return db.session.query(Chapter.id).filter(Chapter.translation_id == self.translation_id, Chapter.chapter == self.chapter+1).scalar()

    @hybrid_property
    def prev_chapter_id(self):
        return db.session.query(Chapter.id).filter(Chapter.translation_id == self.translation_id, Chapter.chapter == self.chapter-1).scalar()
    
    @hybrid_method
    def can_view(self, profile_id: Optional[int], by_link=False):
        if self.privacy_id == 1: 
            return True
        if self.privacy_id == 3 and by_link: 
            return True
        if profile_id:
            if self.creator_id == profile_id: return True

        return False
 
    @can_view.expression
    def can_view(self, profile_id: Optional[int], by_link=False):
        return or_(
            self.privacy_id == 1, 
            and_(self.privacy_id == 3, by_link == True), 
            and_(self.creator_id == profile_id)
        )