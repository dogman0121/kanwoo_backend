from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from typing_extensions import override
from datetime import datetime
from sqlalchemy import Integer, Text, ForeignKey, DateTime, Column, Table, String, Select, func, desc, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app import db, storage
from app.models import Base, File


manga_authors = Table(
    "manga_author",
    db.metadata,
    Column("manga_id", Integer, db.ForeignKey("manga.id")),
    Column("user_id", Integer, db.ForeignKey("profile.id")),
)

manga_artists = Table(
    "manga_artist",
    db.metadata,
    Column("manga_id", Integer, db.ForeignKey("manga.id")),
    Column("profile_id", Integer, db.ForeignKey("profile.id")),
)

manga_publishers = Table(
    "manga_publisher",
    db.metadata,
    Column("manga_id", Integer, db.ForeignKey("manga.id")),
    Column("profile_id", Integer, db.ForeignKey("profile.id")),
)

manga_genres = Table(
    "manga_genre",
    db.metadata,
    Column("genre_id", Integer, db.ForeignKey("genre.id")),
    Column("title_id", Integer, db.ForeignKey("manga.id")),
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

class Translation(Base):
    __tablename__ = "translation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)

    chapters: Mapped[list["Chapter"]] = relationship(uselist=True, lazy="dynamic", back_populates="translation")
    profile: Mapped["Profile"] = relationship("Profile")
    manga: Mapped["Manga"] = relationship("Manga", back_populates="translations")

    @hybrid_property
    def chapters_count(self):
        return self.chapters.count()

    def get_permissions(self, user):
        if user is None:
            return {}
        else:
            if user.id == self.user_id:
                return {
                    "update": True,
                    "delete": True,
                    "add_chapters": True
                }

        return {}

    def to_dict(self, user=None) -> dict:
        return {
            "id": self.id,
            "translator_type": "team" if self.team_id else "user",
            "translator": self.team.to_dict() if self.team_id else self.user.to_dict(),
            "chapters_count": self.chapters_count,
            "permissions": self.get_permissions(user)
        }

    @staticmethod
    def get_by_team(manga_id, team_id):
        return Translation.query.filter_by(manga_id=manga_id, team_id=team_id).scalar()

    @staticmethod
    def get_by_user(manga_id, user_id):
        return Translation.query.filter_by(manga_id=manga_id, user_id=user_id).scalar()

class NameTranslation(Base):
    __tablename__ = "manga_name_translation"

    manga_id: Mapped[int] = mapped_column(Integer, ForeignKey("manga.id"), primary_key=True,
                                          nullable=False)
    lang: Mapped[str] = mapped_column(String(5), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)

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

    def get_url(self) -> str:
        return storage.get_url(f"manga/{self.uuid}{self.ext}")


class Poster(Base):
    __tablename__ = "manga_poster"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    is_deleted: Mapped[bool] = mapped_column(nullable=True, default=False)

    files: Mapped[list["PosterFile"]] = relationship(uselist=True, back_populates="poster")
    manga: Mapped["Manga"] = relationship(back_populates="poster")

    @hybrid_property
    def thumbnail(self):
        file = PosterFile.query.filter_by(poster_uuid=self.uuid, type="thumbnail").scalar()

        if file:
            return file.get_url()

    @hybrid_property
    def small(self):
        file = PosterFile.query.filter_by(poster_uuid=self.uuid, type="thumbnail").scalar()

        if file:
            return file.get_url()

    @hybrid_property
    def medium(self):
        file = PosterFile.query.filter_by(poster_uuid=self.uuid, type="medium").scalar()

        if file:
            return file.get_url()
        
    @hybrid_property
    def large(self):
        file = PosterFile.query.filter_by(poster_uuid=self.uuid, type="large").scalar()

        if file:
            return file.get_url()
        
    @hybrid_property
    def orig(self):
        file = PosterFile.query.filter_by(poster_uuid=self.uuid, type="original").scalar()

        if file:
            return file.get_url()

    def to_dict(self):
        dct =  dict(
            [(file.type, file.get_url()) for file in self.files]
        )
        dct["uuid"] = self.uuid

        return dct

    def get_size(self, size):
        for f in self.files:
            if f.type == size:
                return f
        return None

    def add_file(self, file: PosterFile):
        self.files.append(file)

    @override
    def delete(self):
        for file in self.files:
            storage.delete(f"manga/${self.manga_id}/${file.uuid}{file.ext}")
            file.delete()
        self.delete()

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
    page_size = 20

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
    poster_uuid: Mapped[str] = mapped_column(ForeignKey("manga_poster.uuid"), nullable=True)
    background_uuid: Mapped[str] = mapped_column(ForeignKey("manga_background.uuid"), nullable=True)
    promo_name_uuid: Mapped[str] = mapped_column(ForeignKey("manga_promo_name.uuid"), nullable=True)
    promo_logo_uuid: Mapped[str] = mapped_column(ForeignKey("manga_promo_logo.uuid"), nullable=True)
    promo_background_uuid: Mapped[str] = mapped_column(ForeignKey("manga_promo_background.uuid"), nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda x: datetime.utcnow(), nullable=True)
    verified: Mapped[bool] = mapped_column(default=False)

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
    authors: Mapped[list["Profile"]] = relationship(secondary="manga_author", uselist=True)
    artists: Mapped[list["Profile"]] = relationship(secondary="manga_artist", uselist=True)
    publishers: Mapped[list["Profile"]] = relationship(secondary="manga_publisher", uselist=True)
    creator: Mapped["Profile"] = relationship("Profile")
    # comments: Mapped["Comment"] = relationship("Comment", secondary="manga_comment", back_populates="manga")
    translations: Mapped[list["Translation"]] = relationship("Translation", uselist=True, back_populates="manga")

    @hybrid_property
    def saves_count(self):
        return db.session.execute(Select(func.count(Save.manga_id)).where(Save.manga_id == self.id)).scalar()