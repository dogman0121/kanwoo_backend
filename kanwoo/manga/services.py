from pytils.translit import slugify
from datetime import datetime
from typing import Optional, Tuple, List

from kanwoo.file_storage import FileStorage
from kanwoo.database import DBTransaction
from kanwoo.uuid import UUID
from kanwoo.image import ImageServiceFactory
from kanwoo.entity import FileAction, File
from kanwoo.moderation.services import ModerationService
from kanwoo.moderation.entity import ModerationStatus
from kanwoo.moderation.dto import ModerationStatusUpdateDTO
from kanwoo.profile.entity import AnonymousProfile

from .models import ( 
    Manga, 
    Poster, 
    PosterFile, 
    NameTranslation, 
    Genre, 
    Background, 
    PromoName, 
    PromoLogo, 
    PromoBackground,
    MangaSuggestion
)
from .dto import MangaCreateDTO, MangaUpdateDTO, NameTranslationDTO, MangaSuggestionCreateDTO
from .repositories import MangaRepository, MangaSuggestionRepository
from .exceptions import MangaNotFoundException, MangaUpdateNotAllowedException, MangaDeleteNotAllowedException, MangaInvalidData, MangaCreateNotAllowedException
from .permissions import MangaPolicy


class MangaMediaService:
    """ Service for work with manga media files. Don't check permissions! """

    POSTER_SIZES = {
        "thumbnail": (80, 120),
        "small": (200, 300),
        "medium": (400, 600),
        "large": (600, 900),
    }
    BACKGROUND_SIZE = (1920, 1080)
    PROMO_NAME_SIZE = (420, 360)
    PROMO_LOGO_SIZE = (540, 435)
    PROMO_BACKGROUND_SIZE = (1160, 580)

    def __init__(self, file_storage: FileStorage, image_service_factory: ImageServiceFactory, manga_repo: MangaRepository):
        self.image_service_factory = image_service_factory
        self.manga_repo = manga_repo
        self.file_storage = file_storage

    def __get_path(self, uuid, ext):
        return f"manga/{uuid}{ext}"

    def _save_image(self, image_service, size: Tuple, ext: str) -> str:
        """
            Saves image with uuid

            Parameters:
                file (File): Image file.
                size (tuple[int, int]): Size of the image.
                format (str): Image mimetype. For example: "JPEG" or "WEBP".
                ext (str): File extension. For example: ".webp".

            Returns:
                uuid (str): unique identifier of saved image.

        """
        file_uuid = UUID.generate_uuid()

        img = image_service.resize(size)

        self.file_storage.save(img, f"manga/{file_uuid}{ext}")

        return file_uuid
    
    def set_poster(self, manga: Manga, poster_file: File):
        poster_uuid = UUID.generate_uuid()
        poster = Poster(
            uuid=poster_uuid
        )

        image_service = self.image_service_factory.create(poster_file, "JPEG")

        for quality, size in self.POSTER_SIZES.items():
            poster_version_uuid = self._save_image(image_service, size, ".jpg")

            poster_version = PosterFile(
                uuid=poster_version_uuid,
                path=self.__get_path(poster_version_uuid, ".jpg"),
                poster_uuid=poster_uuid,
                type=quality,
            )

            poster.files.append(poster_version)
                
        
        self.manga_repo.set_poster(manga, poster)

    def set_background(self, manga, background_file: File):
        image_service = self.image_service_factory.create(background_file, "JPEG")

        background_uuid = self._save_image(image_service, self.BACKGROUND_SIZE, ".jpg")

        background = Background(
            uuid=background_uuid,
            path=self.__get_path(background_uuid, ".jpg"),
        )

        self.manga_repo.set_background(manga, background)

        return background_uuid

    def set_promo_name(self, manga, promo_name_file: File):
        image_service = self.image_service_factory.create(promo_name_file, "WEBP")

        promo_name_uuid = self._save_image(image_service, self.PROMO_NAME_SIZE, ".webp")

        promo_name = PromoName(
            uuid=promo_name_uuid,
            path=self.__get_path(promo_name_uuid, ".webp")
        )

        self.manga_repo.set_promo_name(manga, promo_name)

    def set_promo_logo(self, manga, promo_logo_file: File):
        image_service = self.image_service_factory.create(promo_logo_file, "WEBP")

        promo_logo_uuid = self._save_image(image_service, self.PROMO_LOGO_SIZE, ".webp")

        promo_logo = PromoLogo(
            uuid=promo_logo_uuid,
            path=self.__get_path(promo_logo_uuid, ".webp")
        )

        self.manga_repo.set_promo_logo(manga, promo_logo)

    def set_promo_background(self, manga, promo_background_file: File):
        image_service = self.image_service_factory.create(promo_background_file, "WEBP")

        promo_background_uuid = self._save_image(image_service, self.PROMO_BACKGROUND_SIZE, ".webp")

        promo_background = PromoBackground(
            uuid=promo_background_uuid,
            path=self.__get_path(promo_background_uuid, ".webp")
        )

        self.manga_repo.set_promo_background(manga, promo_background)

    def delete_poster(self, manga):
        self.manga_repo.delete_poster(manga)

    def delete_background(self, manga):
        self.manga_repo.delete_background(manga)

    def delete_promo_name(self, manga):
        self.manga_repo.delete_promo_name(manga)

    def delete_promo_logo(self, manga):
        self.manga_repo.delete_promo_logo(manga)

    def delete_promo_background(self, manga):
        self.manga_repo.delete_promo_background(manga)

    def update_poster(self, manga, poster_file: Optional[File]):
        if poster_file:
            self.set_poster(manga, poster_file)
        else:
            self.delete_poster(manga)
    
    def update_background(self, manga, background_file: Optional[File]):
        if background_file:
            self.set_background(manga, background_file)
        else:
            self.delete_background(manga)

    def update_promo_name(self, manga, promo_name_file: Optional[File]):
        if promo_name_file:
            self.set_promo_name(manga, promo_name_file)
        else:
            self.delete_promo_name(manga)

    def update_promo_logo(self, manga, promo_logo_file: Optional[File]):
        if promo_logo_file:
            self.set_promo_logo(manga, promo_logo_file)
        else:
            self.delete_promo_logo(manga)

    def update_promo_background(self, manga, promo_background_file: Optional[File]):
        if promo_background_file:
            self.set_promo_background(manga, promo_background_file)
        else:
            self.delete_promo_background(manga)

class MangaService:

    def __init__(
        self, 
        manga_media_service: MangaMediaService, 
        manga_repo: MangaRepository,
        manga_policy: MangaPolicy,
        moderation_service: ModerationService,
        db_transaction: DBTransaction
    ):
        self.manga_media_service = manga_media_service
        self.manga_repo = manga_repo
        self.manga_policy = manga_policy
        self.moderation_service = moderation_service
        self.db_transaction = db_transaction

    def user_get_manga_by_id(self, profile, manga_id):
        if isinstance(profile, AnonymousProfile):
            manga = self.manga_repo.get_manga_by_id_from_user(None, manga_id)
        else:
            manga = self.manga_repo.get_manga_by_id_from_user(profile, manga_id)

        if manga is None:
            raise MangaNotFoundException

        return manga
    
    def user_get_manga_by_slug(self, profile, slug, by_link=False):
        if isinstance(profile, AnonymousProfile):
            manga = self.manga_repo.get_manga_by_slug_from_user(None, slug, by_link=by_link)
        else:
            manga = self.manga_repo.get_manga_by_slug_from_user(profile, slug, by_link=by_link)

        if manga is None:
            raise MangaNotFoundException()

        return manga
    
    def system_get_manga_by_slug(self, slug):
        manga = self.manga_repo.get_manga_by_slug_from_system(slug)

        if manga is None:
            raise MangaNotFoundException

        return manga
    
    def _get_slug(self, name: str):
        slug = slugify(name)

        # check if slug has been taken
        try:
            i = 1
            while self.system_get_manga_by_slug(slug):
                slug = slugify(name) + str(i)
                i+=1
        except MangaNotFoundException:
            return slug

    def _prepare_name_translations(self, manga: Manga, name_translations: List[NameTranslationDTO]):
        return [
            NameTranslation(
                manga_id=manga.id,
                lang_id=translation.lang_id,
                name=translation.name
            ) for translation in name_translations
        ]
    
    def user_create_manga(self, creator_profile, author_profile, data: MangaCreateDTO):
        if self.manga_policy.can_create(creator_profile, author_profile):
            raise MangaCreateNotAllowedException()

        if not self.manga_repo.check_if_genres_exists(data.genres_ids):
            raise MangaNotFoundException()
        
        if data.slug:
            slug = self._get_slug(data.slug)
        else:
            slug = self._get_slug(data.name)

        manga = Manga(
            slug=slug,
            name=data.name,
            description=data.description,
            type_id=data.type_id,
            status_id=data.status_id,
            year=data.year,
            adult_id=data.adult_id,
            genres=data.genres_ids,
            author_id= author_profile.id if author_profile else None,
            creator_id=creator_profile.id,
            privacy_id=data.privacy_id
        )

        with self.db_transaction:
            if data.poster:
                self.manga_media_service.set_poster(manga, data.poster)
            if data.background:
                self.manga_media_service.set_background(manga, data.background)
            if data.promo_name:
                self.manga_media_service.set_promo_name(manga, data.promo_name)
            if data.promo_logo:
                self.manga_media_service.set_promo_logo(manga, data.promo_logo)
            if data.promo_background:
                self.manga_media_service.set_promo_background(manga, data.promo_background)
                
            manga = self.manga_repo.create_manga(manga)

        moderation_status_dto = ModerationStatusUpdateDTO(
            status_type_id=ModerationStatus.MODERATION.value,
            message="Init status"
        )

        self.moderation_service.system_update_manga_moderation_status(manga, moderation_status_dto)

        return manga

    def user_update_manga(self, profile, manga: Manga, data: MangaUpdateDTO):
        if not self.manga_policy.can_edit(profile, manga):
            raise MangaUpdateNotAllowedException

        if data.slug and manga.slug != data.slug and self.system_get_manga_by_slug(data.slug):
            raise MangaInvalidData(detail={"slug": ["Invalid slug."]})

        name_translations = self._prepare_name_translations(manga, data.name_translations)

        manga.update({
            "name": data.name,
            "name_translations": name_translations,
            "slug": data.slug,
            "description": data.description,
            "type_id": data.type_id,
            "status_id": data.status_id,
            "adult_id": data.adult_id,
            "year": data.year,
            "genres": data.genres_ids,
            "privacy_id": data.privacy_id
        }, commit=False)

        if data.poster_action != FileAction.KEEP:
            self.manga_media_service.update_poster(manga, data.poster)
        if data.background_action != FileAction.KEEP:
            self.manga_media_service.update_background(manga, data.background)
        if data.promo_name_action != FileAction.KEEP:
            self.manga_media_service.update_promo_name(manga, data.promo_name)
        if data.promo_logo_action != FileAction.KEEP:
            self.manga_media_service.update_promo_logo(manga, data.promo_logo)
        if data.promo_background_action != FileAction.KEEP:
            self.manga_media_service.update_promo_background(manga, data.promo_background)

        return self.manga_repo.save_manga(manga)
    
    def _delete_magna(self, manga: Manga):
        self.manga_repo.delete_manga(manga)

    def system_delete_manga(self, manga: Manga):
        pass

    def user_delete_manga(self, profile, manga: Manga):
        if self.manga_policy.can_delete(profile, manga):
            self._delete_manga(manga)
        
        raise MangaDeleteNotAllowedException

    def user_get_profile_manga(self, current_profile, profile):
        return self.manga_repo.get_profile_manga(current_profile.id, profile.id)

    def user_get_manga_edit_form(self, profile, manga: Manga):
        """ Returns edit form data and blocked fields """
        
        return manga, []
    

class MangaSuggestionService:

    def __init__(self, manga_suggestion_repo: MangaSuggestionRepository):
        self.manga_suggestion_repo = manga_suggestion_repo

    def user_create_suggestion(self, profile, data: MangaSuggestionCreateDTO):
        suggestion = MangaSuggestion(
            name=data.name,
            link=data.link,
            comment=data.comment,
            creator_id=data.creator_id
        )

        suggestion.add(commit=True)
        
        return self.manga_suggestion_repo.create_suggestion(suggestion)
        
    def user_get_suggestion_by_id(self, profile, suggestion_id):
        return self.manga_suggestion_repo.get_suggestion_by_id(suggestion_id)

    def user_get_suggestions(self, profile, resolved=None):
        return self.manga_suggestion_repo.get_suggestions(resolved=resolved)

    def user_resolve_suggestion(self, profile, suggestion):
        return self.manga_suggestion_repo.update_suggestion(suggestion, {"resolved_at": datetime.now()})
    
    def user_get_unresolved_suggestions_count(self, profile):
        return self.manga_suggestion_repo.get_active_suggestions_count()
