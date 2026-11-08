from typing import Optional

from sqlalchemy import ForeignKey, and_, or_, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, remote, foreign
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from kanwoo import db
from kanwoo.models import Base, File
from kanwoo.profile.models import Profile
from kanwoo.profile.entity import AnonymousProfile
from kanwoo.permissions import ADMIN_ROLE

from datetime import datetime, timezone

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
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    translation_id: Mapped[int] = mapped_column(ForeignKey("translation.id"), nullable=True)
    privacy_id: Mapped[int] = mapped_column(ForeignKey("privacy.id"), nullable=True)
    

    privacy: Mapped["Privacy"] = relationship()
    pages: Mapped[list["Page"]] = relationship(
        primaryjoin=lambda: and_(Chapter.id==Page.chapter_id, Page.is_deleted==False),
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

    next_chapter: Mapped["Chapter"] = relationship(
        "Chapter",
        primaryjoin=lambda: and_(
            remote(Chapter.translation_id) == foreign(Chapter.translation_id),
            or_(
                remote(Chapter.chapter) > foreign(Chapter.chapter),
                and_(
                    remote(Chapter.chapter) == foreign(Chapter.chapter),
                    remote(Chapter.extra_number) > foreign(Chapter.extra_number)
                ),
                and_(
                    remote(Chapter.chapter) == foreign(Chapter.chapter),
                    foreign(Chapter.extra_number).is_(None),
                    remote(Chapter.extra_number).is_not(None)
                )
            )
        ),
        order_by=lambda: (Chapter.chapter.asc(), Chapter.extra_number.asc().nulls_last()),
        uselist=False,
        viewonly=True
    )

    prev_chapter: Mapped["Chapter"] = relationship(
        "Chapter",
        primaryjoin=lambda: and_(
            remote(Chapter.translation_id) == foreign(Chapter.translation_id),
            or_(
                remote(Chapter.chapter) < foreign(Chapter.chapter),
                and_(
                    remote(Chapter.chapter) == foreign(Chapter.chapter),
                    remote(Chapter.extra_number) < foreign(Chapter.extra_number)
                ),
                and_(
                    remote(Chapter.chapter) == foreign(Chapter.chapter),
                    foreign(Chapter.extra_number).is_not(None),
                    remote(Chapter.extra_number).is_(None)
                )
            )
        ),
        order_by=lambda: (Chapter.chapter.desc(), Chapter.extra_number.desc().nulls_last()),
        uselist=False,
        viewonly=True
    )

    @hybrid_property
    def next_chapter_id(self):
        if self.next_chapter:
            return self.next_chapter.id

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