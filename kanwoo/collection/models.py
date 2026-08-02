from sqlalchemy import ForeignKey, and_, or_, func, select, exists
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from datetime import datetime
from typing import Optional


from kanwoo.entity import Privacy
from kanwoo.models import Base
from kanwoo.manga.models import Manga


class Collection(Base):
    __tablename__ = 'collection'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    privacy_id: Mapped[str] = mapped_column(ForeignKey("privacy.id"), nullable=True)

    manga: Mapped[list["Manga"]] = relationship(
                                            "Manga", uselist=True,
                                            primaryjoin="Collection.id == CollectionManga.collection_id",
                                            secondary="collection_manga",
                                            secondaryjoin="CollectionManga.manga_id == Manga.id",
                                            back_populates="collections"
                                        )
    creator: Mapped["Profile"] = relationship("Profile", back_populates="collections")
    privacy: Mapped["Privacy"] = relationship("Privacy")

    @hybrid_method
    def can_view(self, profile_id, by_link=False):
        if self.privacy_id == Privacy.PUBLIC.value: 
            return True
        if self.privacy_id == Privacy.PRIVATE.value and by_link: 
            return True
        if profile_id:
            if self.creator_id == profile_id: return True

        return False
 
    @can_view.expression
    def can_view(self, profile_id: Optional[int], by_link=False):
        return or_(
            self.privacy_id == Privacy.PUBLIC.value, # Публичная манга
            and_(self.privacy_id == Privacy.BY_LINK.value, by_link == True), # Доступ по ссылке 
            and_(self.creator_id == profile_id) # Пользователь - это создатель
        )

    @hybrid_method
    def contain_manga(self, manga_slug):
        return any(
            m.slug == manga_slug for m in self.manga
        )
    
    @contain_manga.expression
    def contain_manga(self, manga_slug):
        return (
            select(Manga.id).join(
                CollectionManga,
                CollectionManga.manga_id == Manga.id
            )
            .where(
                Manga.slug == manga_slug,
                CollectionManga.collection_id == self.id
            ).exists()
        )
    
    @hybrid_property
    def manga_count(self):
        if self.manga:
            return len(self.manga)
        
        return 0

    @manga_count.expression
    def manga_count(self):
        return select(func.count(
            select(
                Manga.id
            )
            .join(CollectionManga)
            .filter(CollectionManga.collection_id == self.id)
        ))
    
class CollectionManga(Base):
    __tablename__ = 'collection_manga'

    collection_id: Mapped[int] = mapped_column(ForeignKey("collection.id", ondelete="CASCADE"), primary_key=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id", ondelete="CASCADE"), primary_key=True)


class CollectionSave(Base):
    __tablename__ = 'collection_save'

    collection_id: Mapped[int] = mapped_column(ForeignKey("collection.id", ondelete="CASCADE"), primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id", ondelete="CASCADE"), primary_key=True)