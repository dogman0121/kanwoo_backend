from typing import Optional
from typing_extensions import override
from datetime import datetime

from sqlalchemy import Integer, Text, ForeignKey, DateTime, Column, Table, String, select, and_, or_
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import Mapped, mapped_column, relationship

from kanwoo import db
from kanwoo.permissions import ADMIN_ROLE
from kanwoo.entity import  Privacy
from kanwoo.models import Base, File
from kanwoo.moderation.models import MangaModerationStatus
from kanwoo.moderation.entity import ModerationStatus
from kanwoo.profile.models import Profile
from kanwoo.profile.entity import AnonymousProfile


manga_genres = Table(
    "manga_genre",
    db.metadata,
    Column("genre_id", Integer, db.ForeignKey("genre.id")),
    Column("manga_id", Integer, db.ForeignKey("manga.id")),
)

class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }

class Type(Base):
    __tablename__ = "type"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }

class Status(Base):
    __tablename__ = "status"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }

class Adult(Base):
    __tablename__ = "adult"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }

class Save(Base):
    __tablename__ = "manga_save"

    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    def to_dict(self, user=None) -> dict:
        return {
            "id": self.id,
            "translator_type": "team" if self.team_id else "user",
            "translator": self.team.to_dict() if self.team_id else self.user.to_dict(),
            "chapters_count": self.chapters_count,
            "permissions": self.get_permissions(user)
        }

class NameTranslation(Base):
    __tablename__ = "manga_name_translation"

    manga_id: Mapped[int] = mapped_column(Integer, ForeignKey("manga.id"), primary_key=True,
                                          nullable=False)
    lang_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    lang: Mapped["Language"] = relationship("Language")

    def to_dict(self):
        return {
            "lang": self.lang,
            "name": self.name,
        }

class PosterFile(Base, File):
    __tablename__ = "manga_poster_file"
    uuid: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=True)
    poster_uuid: Mapped[str] = mapped_column(ForeignKey("manga_poster.uuid", ondelete="CASCADE"), nullable=False)

    poster: Mapped["Poster"] = relationship("Poster", back_populates="files")


class Poster(Base):
    __tablename__ = "manga_poster"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    is_deleted: Mapped[bool] = mapped_column(nullable=True, default=False)

    files: Mapped[list["PosterFile"]] = relationship(
        primaryjoin=("and_(Poster.uuid==PosterFile.poster_uuid, PosterFile.is_deleted==False)"),
        uselist=True, 
        back_populates="poster"
        )
    manga: Mapped["Manga"] = relationship(back_populates="poster")

    def _get_size(self, size):
        for f in self.files:
            if f.type == size:
                return f
        return None

    @hybrid_property
    def thumbnail(self): return self._get_size("thumbnail")

    @hybrid_property
    def small(self): return self._get_size("small")

    @hybrid_property
    def medium(self): return self._get_size("medium")

    @hybrid_property
    def large(self): return self._get_size("large")

    @hybrid_property
    def original(self): return self._get_size("original")

    @override
    def delete(self):
        self.is_deleted = True
        for file in self.files:
            file.delete()

class Background(Base, File):
    __tablename__ = "manga_background"

    manga: Mapped["Manga"] = relationship(back_populates="background")

class PromoName(Base, File):
    __tablename__ = "manga_promo_name"

    manga: Mapped["Manga"] = relationship(back_populates="promo_name")

class PromoLogo(Base, File):
    __tablename__ = "manga_promo_logo"

    manga: Mapped["Manga"] = relationship(back_populates="promo_logo")

class PromoBackground(Base, File):
    __tablename__ = "manga_promo_background"

    manga: Mapped["Manga"] = relationship(back_populates="promo_background")

class Manga(Base):
    __tablename__ = 'manga'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("type.id"), nullable=True)
    status_id: Mapped[Optional[int]] = mapped_column(ForeignKey("status.id"), nullable=True)
    year: Mapped[Optional[int]] = mapped_column(nullable=True)
    views: Mapped[Optional[int]] = mapped_column(default=0)
    adult_id: Mapped[Optional[int]] = mapped_column(ForeignKey("adult.id"), nullable=True)
    poster_uuid: Mapped[str] = mapped_column(ForeignKey("manga_poster.uuid", ondelete="SET NULL"), nullable=True)
    background_uuid: Mapped[str] = mapped_column(ForeignKey("manga_background.uuid", ondelete="SET NULL"), nullable=True)
    promo_name_uuid: Mapped[str] = mapped_column(ForeignKey("manga_promo_name.uuid", ondelete="SET NULL"), nullable=True)
    promo_logo_uuid: Mapped[str] = mapped_column(ForeignKey("manga_promo_logo.uuid", ondelete="SET NULL"), nullable=True)
    promo_background_uuid: Mapped[str] = mapped_column(ForeignKey("manga_promo_background.uuid", ondelete="SET NULL"), nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.utcnow(), nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
    privacy_id: Mapped[int] = mapped_column(ForeignKey("privacy.id"), nullable=True)

    privacy: Mapped["Privacy"] = relationship("Privacy")
    name_translations: Mapped[list["NameTranslation"]] = relationship(
        cascade="save-update, merge, delete, delete-orphan")
    type: Mapped["Type"] = relationship()
    status: Mapped["Status"] = relationship()
    background: Mapped["Background"] = relationship(
        primaryjoin="and_(Manga.background_uuid == Background.uuid, Background.is_deleted == False)",
        back_populates="manga",
        foreign_keys=[background_uuid]
    )
    poster: Mapped["Poster"] = relationship(
        primaryjoin="and_(Manga.poster_uuid == Poster.uuid, Poster.is_deleted == False)",
        back_populates="manga",
        foreign_keys=[poster_uuid]
    )
    promo_name: Mapped["PromoName"] = relationship(
        primaryjoin="and_(Manga.promo_name_uuid == PromoName.uuid, PromoName.is_deleted == False)",
        back_populates="manga",
        foreign_keys=[promo_name_uuid]
    )
    promo_background: Mapped["PromoBackground"] = relationship(
        primaryjoin="and_(Manga.promo_background_uuid == PromoBackground.uuid, PromoBackground.is_deleted == False)",
        back_populates="manga",
        foreign_keys=[promo_background_uuid]
    )
    promo_logo: Mapped["PromoLogo"] = relationship(
        primaryjoin="and_(Manga.promo_logo_uuid == PromoLogo.uuid, PromoLogo.is_deleted == False)",
        back_populates="manga",
        foreign_keys=[promo_logo_uuid]
    )
    adult: Mapped["Adult"] = relationship()
    genres: Mapped[list["Genre"]] = relationship("Genre", secondary="manga_genre")
    creator: Mapped["Profile"] = relationship("Profile", foreign_keys=[creator_id])
    author: Mapped["Profile"] = relationship("Profile", foreign_keys=[author_id])
    translations: Mapped[list["Translation"]] = relationship("Translation", uselist=True, back_populates="manga")
    moderation_history: Mapped[list[MangaModerationStatus]] = relationship(
        primaryjoin="Manga.id==MangaModerationStatus.manga_id",
        order_by=MangaModerationStatus.created_at.desc(),
        viewonly=True
    )

    @hybrid_property
    def moderation_status(self):
        if self.moderation_history:
            return self.moderation_history[0]
        return None

    @hybrid_property
    def moderation_status_type_id(self):
        if self.moderation_history:
            return self.moderation_history[0].id
        return None
    
    @moderation_status_type_id.expression
    def moderation_status_type_id(cls):
        subq = (
            select(MangaModerationStatus.status_type_id)
            .where(MangaModerationStatus.manga_id == cls.id)
            .order_by(MangaModerationStatus.created_at.desc())
            .limit(1).scalar_subquery()
        )
        return subq

    
    @hybrid_method
    def can_view(self, profile: Profile | AnonymousProfile, by_link=False):
        if isinstance(profile, Profile) and profile.role >= ADMIN_ROLE:
            return True
        if isinstance(profile, Profile) and profile.id:
            if self.author_id == profile.id: return True
        if self.moderation_status_type_id != ModerationStatus.APPROVED.value:
            return False
        if self.privacy_id == Privacy.PUBLIC.value: 
            return True
        if self.privacy_id == Privacy.PRIVATE.value and by_link: 
            return True

        return False
 
    @can_view.expression
    def can_view(self, profile: Optional[Profile], by_link=False):
        if isinstance(profile, Profile):
            return or_(
                profile.role >= ADMIN_ROLE,
                and_(
                    self.moderation_status_type_id == ModerationStatus.APPROVED.value,
                    or_(
                        self.privacy_id == Privacy.PUBLIC.value, # Публичная манга
                        and_(self.privacy_id == Privacy.BY_LINK.value, by_link == True), # Доступ по ссылке 
                        and_(self.author_id == profile.id) # Пользователь - это создатель
                    )
                )
            )
        
        return and_(
            self.moderation_status_type_id == ModerationStatus.APPROVED.value,
            or_(
                self.privacy_id == Privacy.PUBLIC.value, # Публичная манга
                and_(self.privacy_id == Privacy.BY_LINK.value, by_link == True) # Доступ по ссылке 
            )
        )

class MangaSuggestion(Base):
    __tablename__ = "manga_suggestion"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column()
    link: Mapped[str] = mapped_column()
    comment: Mapped[str] = mapped_column(nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.now())
    resolver_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
    resolved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    creator: Mapped["Profile"] = relationship(foreign_keys=[creator_id])

    resolver: Mapped["Profile"] = relationship(foreign_keys=[resolver_id])
