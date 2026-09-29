from typing import Optional

from sqlalchemy import ForeignKey, and_, or_, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from kanwoo import db
from kanwoo.models import Base, File
from kanwoo.profile.models import Profile
from kanwoo.profile.entity import AnonymousProfile
from kanwoo.permissions import ADMIN_ROLE

from datetime import datetime

class Page(Base, File):
    __tablename__ = "page"

    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id", ondelete="SET NULL"), nullable=True)
    width: Mapped[int] = mapped_column()
    height: Mapped[int] = mapped_column()
    order: Mapped[int] = mapped_column(nullable=False)


class Chapter(Base):
    __tablename__ = "chapter"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    tome: Mapped[int] = mapped_column(nullable=True)
    chapter: Mapped[int] = mapped_column(nullable=False)
    extra_number: Mapped[int] = mapped_column(nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    translation_id: Mapped[int] = mapped_column(ForeignKey("translation.id"), nullable=True)
    privacy_id: Mapped[int] = mapped_column(ForeignKey("privacy.id"), nullable=True)

    privacy: Mapped["Privacy"] = relationship()
    pages: Mapped[list["Page"]] = relationship(
        primaryjoin="and_(Chapter.id==Page.chapter_id, Page.is_deleted==False)",
        order_by="Page.order"
    )
    translation: Mapped["Translation"] = relationship(back_populates="chapters")
    creator: Mapped["Profile"] = relationship()
    manga: Mapped["Manga"] = relationship("Manga",  primaryjoin="Chapter.translation_id == Translation.id", secondary="translation",
                         secondaryjoin="Translation.manga_id == Manga.id", viewonly=True)

    @hybrid_property
    def next_chapter(self):
        rn = func.row_number().over(
            partition_by=Chapter.translation_id,
            order_by=(
                Chapter.chapter.asc(),
                Chapter.extra_number.asc().nulls_last(),
            ),
        ).label("rn")

        subq = (
            select(Chapter.id.label("chapter_id"), rn)
            .where(Chapter.translation_id == self.translation_id)
            .subquery()
        )

        current_rn = db.session.execute(
            select(subq.c.rn).where(subq.c.chapter_id == self.id)
        ).scalar()

        if current_rn is None:
            return None

        stmt = (
            select(Chapter)
            .join(subq, Chapter.id == subq.c.chapter_id)
            .where(subq.c.rn == current_rn + 1)
        )
        return db.session.execute(stmt).scalars().first()

    @hybrid_property
    def next_chapter_id(self):
        if self.next_chapter:
            return self.next_chapter.id

    @hybrid_property
    def prev_chapter(self):
        rn = func.row_number().over(
            partition_by=Chapter.translation_id,
            order_by=(
                Chapter.chapter.asc(),
                Chapter.extra_number.asc().nulls_last()
            )
        ).label("rn")

        subq = (
            select(
                Chapter.id.label("chapter_id"),
                Chapter.translation_id.label("translation_id"),
                rn,
            )
            .where(Chapter.translation_id == self.translation_id)
            .subquery()
        )

        current_rn = (
            select(subq.c.rn)
            .where(subq.c.chapter_id == self.id)
            .scalar_subquery()
        )

        stmt = (
            select(Chapter)
            .join(subq, Chapter.id == subq.c.chapter_id)
            .where(subq.c.rn == current_rn - 1)
        )

        return db.session.execute(stmt).scalars().first()

    @hybrid_property
    def prev_chapter_id(self):
        return self.prev_chapter.id

    @hybrid_property
    def is_last(self):
        return self.next_chapter is None
    
    @hybrid_method
    def can_view(self, profile: Profile | AnonymousProfile, by_link=False):
        if isinstance(profile, Profile) and profile.role >= ADMIN_ROLE:
            return True
        if self.privacy_id == 1: 
            return True
        if self.privacy_id == 3 and by_link: 
            return True
        if isinstance(profile, Profile):
            if self.creator_id == profile.id: return True

        return False
 
    @can_view.expression
    def can_view(self, profile: Profile | AnonymousProfile, by_link=False):
        if isinstance(profile, Profile):
            return or_(
                profile.role >= ADMIN_ROLE,
                self.privacy_id == 2, 
                and_(self.privacy_id == 3, by_link == True), 
                and_(self.creator_id == profile.id)
            )
        
        return or_(
            self.privacy_id == 2, 
            and_(self.privacy_id == 3, by_link == True)
        ) 

    @hybrid_property
    def pages_count(self):
        return len(self.pages)