from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import ForeignKey, DateTime, or_, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional

from kanwoo.profile.models import Profile
from kanwoo.models import Privacy
from kanwoo.models import Base
from kanwoo.permissions import ADMIN_ROLE


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
    chapters: Mapped[list["Chapter"]] = relationship(uselist=True, lazy="dynamic", back_populates="translation")
    owner: Mapped["Profile"] = relationship("Profile", foreign_keys=[owner_id])
    creator: Mapped["Profile"] = relationship("Profile", foreign_keys=[creator_id])
    manga: Mapped["Manga"] = relationship("Manga", back_populates="translations")

    @hybrid_property
    def chapters_count(self):
        return self.chapters.count()
    
    @hybrid_method
    def can_view(self, profile: Optional[Profile], by_link=False):
        if profile and profile.role >= ADMIN_ROLE:
            return True
        if profile and profile.id:
            if self.author_id == profile.id: return True
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
                and_(self.author_id == profile.id) # Пользователь - это создатель
            )
        )