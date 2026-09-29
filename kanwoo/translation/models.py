from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import ForeignKey, DateTime, or_, and_, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional


from kanwoo.profile.models import Profile
from kanwoo.entity import Privacy
from kanwoo.models import Base
from kanwoo.permissions import ADMIN_ROLE
from kanwoo.chapter.models import Chapter

class Translation(Base):
    __tablename__ = "translation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=True)
    privacy_id: Mapped[int] = mapped_column(ForeignKey("privacy.id"), nullable=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"))
    lang_id: Mapped[str] = mapped_column(ForeignKey("language.id"), nullable=True)
    is_official: Mapped[bool] = mapped_column(default=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.utcnow(), nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)

    lang: Mapped["Language"] = relationship("Language")
    privacy: Mapped["Privacy"] = relationship("Privacy")
    chapters: Mapped[list["Chapter"]] = relationship(
        uselist=True, 
        lazy="dynamic", 
        back_populates="translation", 
        order_by=(Chapter.chapter.asc(), Chapter.extra_number.asc().nulls_first())
    )
    owner: Mapped["Profile"] = relationship("Profile", foreign_keys=[owner_id])
    creator: Mapped["Profile"] = relationship("Profile", foreign_keys=[creator_id])
    manga: Mapped["Manga"] = relationship("Manga", back_populates="translations")

    @hybrid_property
    def chapters_count(self):
        return self.chapters.count()
    
    @chapters_count.expression
    def chapters_count(cls):
        return (
            select(
                func.count(Chapter.id))
            .filter(Chapter.translation_id == cls.id)
            .correlate(Translation)
            .scalar_subquery()
        )
    
    @hybrid_property
    def last_chapter_id(self):
        if (len(self.chapter)):
            return self.chapters[-1].id

    @last_chapter_id.expression
    def last_chapter_id(self):
        return (
            select(Chapter.id)
            .join(
                Translation, 
                Chapter.translation_id == Translation.id
            )
            .order_by(
                Chapter.chapter.desc(),
                Chapter.extra_number.desc().nulls_last()
            )
            .limit(1)
            .scalar_subquery()
        )
    
    @hybrid_method
    def can_view(self, profile: Optional[Profile], by_link=False):
        if profile and profile.role >= ADMIN_ROLE:
            return True
        if profile and profile.id:
            if self.owner == profile.id: return True
        if self.privacy_id == Privacy.PUBLIC.value: 
            return True
        if self.privacy_id == Privacy.PRIVATE.value and by_link: 
            return True

        return False
 
    @can_view.expression
    def can_view(self, profile: Optional[Profile], by_link=False):
        return or_(
            profile.role >= ADMIN_ROLE,
            or_(
                self.privacy_id == Privacy.PUBLIC.value, # Публичная манга
                and_(self.privacy_id == Privacy.BY_LINK.value, by_link == True), # Доступ по ссылке 
                and_(self.owner_id == profile.id) # Пользователь - это создатель
            )
        )

class TranslationSubscribtion(Base):
    __tablename__ = "translation_subscribe"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    translation_id: Mapped[int] = mapped_column(ForeignKey("translation.id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))