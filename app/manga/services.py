from pytils.translit import slugify
from typing import Optional, Tuple

from app.logs import logging

from app import db, storage
from app.uuid import UUID
from app.image import ImageService
from app.entity import FileAction, File

from .models import (
    Translation, 
    Manga, 
    Poster, 
    PosterFile, 
    NameTranslation, 
    Genre, 
    Background, 
    PromoName, 
    PromoLogo, 
    PromoBackground
)
from .dto import MangaCreateDTO, MangaUpdateDTO
from .repositories import MangaRepository
from .exceptions import MangaNotFoundException, MangaSaveImageException
from .permissions import MangaPolicy
from .exceptions import MangaUpdateNotAllowedException

class TranslationService:
    def __init__(self):
        pass

    @staticmethod
    def get_translation(manga=None, team=None, user=None):
        if team and manga:
            return Translation.query.filter_by(manga_id=manga.id, team_id=team.id).first()
        elif user and manga:
            return Translation.query.filter_by(manga_id=manga.id, user_id=user.id).first()
        else:
            raise ValueError("You need to specify either team or user")

    @staticmethod
    def get_or_create_translation(manga=None, team=None, user=None):
        translation = TranslationService.get_translation(manga=manga, team=team, user=user)
        if translation:
            return translation

        if team and manga:
            new_translation = Translation(manga_id=manga.id, team_id=team.id)
            db.session.add(new_translation)
            db.session.commit()
        elif user and manga:
            new_translation = Translation(manga_id=manga.id, user_id=user.id)
            db.session.add(new_translation)
            db.session.commit()
        else:
            raise ValueError("You need to specify either team or user")

        return new_translation


class MangaService:
    poster_sizes = {
        "thumbnail": (80, 120),
        "small": (200, 300),
        "medium": (400, 600),
        "large": (600, 900),
    }

    def __init__(self, profile):
        self.profile = profile

    def get_manga_by_id(self, manga_id):
        manga = MangaRepository.get_by_id(manga_id)

        if manga is None:
            raise MangaNotFoundException

        return manga
    
    @staticmethod
    def get_manga_by_slug(slug):
        manga = MangaRepository.get_by_slug(slug)

        if manga is None:
            raise MangaNotFoundException

        return manga

    def create_manga(self, data: MangaCreateDTO):
        slug = slugify(data.name)

        # check if slug has been taken
        try:
            i = 1
            while self.get_manga_by_slug(slug):
                slug = slugify(data.name) + str(i)
                i+=1
        except MangaNotFoundException:
            pass
        
        manga = Manga(
            slug=slug,
            name=data.name,
            creator=self.profile
        )

        manga = MangaRepository.create_manga(manga)

        return manga
    
    def _update_poster(self, manga: Manga, poster_file: Optional[File], poster_action: FileAction):
        if poster_action == FileAction.DELETE:
            MangaRepository().delete_poster(manga)
        elif poster_action == FileAction.UPDATE:
            try:
                poster_uuid = UUID.generate_uuid()
                poster = Poster(
                    uuid = poster_uuid,
                )

                for quality, size in self.poster_sizes.items():
                    poster_version_file = ImageService(poster_file, output_format="JPEG").resize(size)
                    poster_version_uuid = UUID.generate_uuid()

                    poster_version = PosterFile(
                        uuid=poster_version_uuid,
                        poster_uuid=poster_uuid,
                        type=quality,
                        ext=".jpg"
                    )
                    storage.save(poster_version_file, f"manga/{poster_version_uuid}.jpg")
                    poster.files.append(poster_version)
                
                MangaRepository().set_poster(manga, poster)
            except Exception as e:
                raise MangaSaveImageException("Can't save manga poster")

    def __update_manga_image(
            self,
            manga: Manga, 
            attribute: str, 
            file: Optional[File], 
            action: FileAction,
            fileClass: type, 
            format: str,
            ext: str,
            size: Tuple[int, int],
        ):
        if action == FileAction.KEEP:
            pass
        elif action == FileAction.DELETE:
            if getattr(manga, attribute):
                old_image = getattr(manga, attribute)
                setattr(manga, attribute, None)
                old_image.is_deleted = True
        elif action == FileAction.UPDATE:
            if getattr(manga, attribute):
                old_image = getattr(manga, attribute)
                old_image.is_deleted = True
            
            file_uuid = UUID.generate_uuid()
            processed_image = ImageService(file, output_format=format).resize(size)
            file_object = fileClass(
                uuid=file_uuid,
                ext=ext
            )
            
            storage.save(processed_image, f"manga/{file_uuid}{ext}")
            setattr(manga, attribute, file_object)
        
            return file_object

    def _update_background(self, manga: Manga, background_file: Optional[File], background_action: FileAction):
        self.__update_manga_image(
            manga,
            "background",
            background_file,
            background_action,
            Background,
            "JPEG",
            ".jpg",
            (1920, 1080)
        )

    def _update_promo_name(self, manga: Manga, promo_name: Optional[File], promo_name_action: FileAction):
        self.__update_manga_image(
            manga,
            "promo_name",
            promo_name,
            promo_name_action,
            PromoName,
            "WEBP",
            ".webp",
            (420, 360)
        )

    def _update_promo_logo(self, manga: Manga, promo_logo: Optional[File], promo_logo_action: FileAction):
        self.__update_manga_image(
            manga,
            "promo_logo",
            promo_logo,
            promo_logo_action,
            PromoLogo,
            "WEBP",
            ".webp",
            (540, 435)
        )

    def _update_promo_background(self, manga: Manga, promo_background: File, promo_background_action: FileAction):
        self.__update_manga_image(
            manga,
            "promo_background",
            promo_background,
            promo_background_action,
            PromoBackground,
            "WEBP",
            ".webp",
            (1160, 580)
        )

    def update_manga(self, manga: Manga, data: MangaUpdateDTO):
        if not MangaPolicy(self.profile).can_edit(manga):
            raise MangaUpdateNotAllowedException

        self._update_poster(manga, data.poster, data.poster_action)

        self._update_background(manga, data.background, data.background_action)

        self._update_promo_name(manga, data.promo_name, data.promo_name_action)

        self._update_promo_logo(manga, data.promo_logo, data.promo_logo_action)

        self._update_promo_background(manga, data.promo_background, data.promo_background_action)

        name_translations = []
        for translation in data.name_translations:
            t = NameTranslation(
                lang=translation.lang,
                name=translation.name
            )

            name_translations.append(t)
        
        genres = []
        for genre in data.genres:
            g = Genre.get(genre)
            genres.append(g)

        manga.update({
            "name": data.name,
            "slug": data.slug,
            "description": data.description,
            "type_id": data.type,
            "status_id": data.status,
            "adult_id": data.adult,
            "year": data.year,
            "genres": genres,
        }, commit=False)

        db.session.commit()

        return manga