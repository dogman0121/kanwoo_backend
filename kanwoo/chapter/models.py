from typing import Optional

from sqlalchemy import ForeignKey, and_, or_, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, object_session, aliased
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from kanwoo import db
from kanwoo.models import BaseModel, FileModelMixin
from kanwoo.profile.models import Profile
from kanwoo.profile.entity import AnonymousProfile
from kanwoo.permissions import ADMIN_ROLE

from datetime import datetime, timezone

class Page(BaseModel, FileModelMixin):
    __tablename__ = "page"

    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id", ondelete="SET NULL"), nullable=True)
    width: Mapped[int] = mapped_column()
    height: Mapped[int] = mapped_column()
    order: Mapped[int] = mapped_column(nullable=False)

class ChapterPage(BaseModel):
    __tablename__ = "chapter_page"

    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))
    file_uuid: Mapped[int]
    width: Mapped[int] = mapped_column()
    height: Mapped[int] = mapped_column()
    order: Mapped[int] = mapped_column()


class Chapter(BaseModel):
    __tablename__ = "chapter"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    tome: Mapped[int] = mapped_column(nullable=True)
    chapter: Mapped[int] = mapped_column(nullable=False)
    extra_number: Mapped[int] = mapped_column(nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=True
    )
    translation_id: Mapped[int] = mapped_column(ForeignKey("translation.id"), nullable=True)
    privacy_id: Mapped[int] = mapped_column(ForeignKey("privacy.id"), nullable=True)
    

    privacy: Mapped["Privacy"] = relationship()
    pages: Mapped[list["Page"]] = relationship(
        primaryjoin="and_(Chapter.id==Page.chapter_id, Page.is_deleted == False)",
        order_by="Page.order"
    )
    translation: Mapped["Translation"] = relationship(back_populates="chapters")
    creator: Mapped["Profile"] = relationship()
    manga: Mapped["Manga"] = relationship(
        "Manga",  
        primaryjoin="Chapter.translation_id == Translation.id", 
        secondary="translation",
        secondaryjoin="Translation.manga_id == Manga.id", 
        viewonly=True
    )

    @hybrid_property
    def next_chapter(self):
        if self.translation_id is None:
            return None
        
        session = object_session(self)
        if session is None:
            return None
        
        # Учитываем случай, когда self.extra_number is None
        if self.extra_number is None:
            extra_cond = and_(
                Chapter.chapter == self.chapter,
                Chapter.extra_number.is_not(None)
            )
        else:
            extra_cond = and_(
                Chapter.chapter == self.chapter,
                Chapter.extra_number > self.extra_number
            )

        stmt = (
            select(Chapter)
            .where(
                Chapter.translation_id == self.translation_id,
                Chapter.id != self.id,
                or_(Chapter.chapter > self.chapter, extra_cond),
            )
            .order_by(Chapter.chapter.asc(), Chapter.extra_number.asc().nulls_first())
            .limit(1)
        )
        return session.execute(stmt).scalar_one_or_none()

    @next_chapter.expression
    def next_chapter(cls):
        OtherChapter = aliased(cls)
        stmt = (
            select(OtherChapter.id)
            .where(
                OtherChapter.translation_id == cls.translation_id,
                OtherChapter.id != cls.id,
                or_(
                    OtherChapter.chapter > cls.chapter,
                    and_(
                        OtherChapter.chapter == cls.chapter,
                        or_(
                            and_(cls.extra_number.is_(None), OtherChapter.extra_number.is_not(None)),
                            OtherChapter.extra_number > cls.extra_number
                        )
                    )
                )
            )
            .order_by(OtherChapter.chapter.asc(), OtherChapter.extra_number.asc().nulls_first())
            .limit(1)
            .correlate(cls)
        )
        return stmt.scalar_subquery()

    @hybrid_property
    def next_chapter_id(self):
        next_ch = self.next_chapter
        return next_ch.id if next_ch else None

    @hybrid_property
    def prev_chapter(self):
        if self.translation_id is None:
            return None
        
        session = object_session(self)
        if session is None:
            return None
        
        # Если extra_number is None, то экстры с меньшим номером быть не может
        if self.extra_number is None:
            condition = Chapter.chapter < self.chapter
        else:
            condition = or_(
                Chapter.chapter < self.chapter,
                and_(
                    Chapter.chapter == self.chapter,
                    or_(
                        Chapter.extra_number < self.extra_number,
                        Chapter.extra_number.is_(None)
                    )
                )
            )

        stmt = (
            select(Chapter)
            .where(
                Chapter.translation_id == self.translation_id,
                Chapter.id != self.id,
                condition,
            )
            .order_by(Chapter.chapter.desc(), Chapter.extra_number.desc().nulls_last())
            .limit(1)
        )
        return session.execute(stmt).scalar_one_or_none()

    @prev_chapter.expression
    def prev_chapter(cls):
        OtherChapter = aliased(cls)
        stmt = (
            select(OtherChapter.id)
            .where(
                OtherChapter.translation_id == cls.translation_id,
                OtherChapter.id != cls.id,
                or_(
                    OtherChapter.chapter < cls.chapter,
                    and_(
                        OtherChapter.chapter == cls.chapter,
                        cls.extra_number.is_not(None),
                        or_(
                            OtherChapter.extra_number < cls.extra_number,
                            OtherChapter.extra_number.is_(None)
                        )
                    )
                )
            )
            .order_by(OtherChapter.chapter.desc(), OtherChapter.extra_number.desc().nulls_last())
            .limit(1)
            .correlate(cls)
        )
        return stmt.scalar_subquery()

    @hybrid_property
    def prev_chapter_id(self):
        prev_ch = self.prev_chapter
        return prev_ch.id if prev_ch else None

    @hybrid_property
    def is_last(self):
        next_ch = self.next_chapter
        return next_ch is None
    
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