from typing import Optional

from kanwoo.manga.models import Manga
from kanwoo.profile.models import Profile
from kanwoo.chapter.services import ChapterService

from .permissions import TranslationPolicy
from .dto import TranslationUpdateDTO, TranslationCreateDTO
from .models import Translation
from .repositories import TranslationRepository
from .exceptions import (
    TranslationNotFoundException, 
    TranslationAlreadyExistsException, 
    TranslationUpdateNotAllowed,
    TranslationChaptersForbidden,
    TranslationDeleteNotAllowed
)

class TranslationService:

    def __init__(
        self, 
        translation_repo: TranslationRepository,
        translation_policy: TranslationPolicy
    ):
        self.translation_repo = translation_repo
        self.translation_policy = translation_policy

    def user_get_translation_by_id(self, profile, translation_id):
        translation = self.translation_repo.get_translation_by_id(translation_id)

        if translation is None:
            raise TranslationNotFoundException
        
        return translation

    def add_translation(self):
        pass

    def user_get_manga_translations(self, profile, manga: Manga, official: Optional[bool] = None):
        if official is None:
            translations = self.translation_repo.get_manga_translations(manga.id, official=True)

            if len(translations) == 0:
                return self.translation_repo.get_manga_translations(manga.id, official=False)
            
            return translations
        else:
            return self.translation_repo.get_manga_translations(manga.id, official=official)
        
    def user_create_manga_translation(self, profile, manga: Manga, data):
        if self.translation_repo.check_translation_with_same_lang(profile.id, manga.id, data.lang_id):
            raise TranslationAlreadyExistsException
        
        translation = Translation(
            name=data.name,
            lang_id=data.lang_id,
            manga_id=manga.id,
            privacy_id=data.privacy_id,
            creator_id=profile.id,
            is_official=data.is_official
        )
        
        return self.translation_repo.create_translation(translation)
    
    def user_get_profile_translations(self, profile: Profile):
        return self.translation_repo.get_profile_translations(profile.id)
    
    def user_update_translation(self, profile, translation: Translation, data: TranslationUpdateDTO):
        if not self.translation_policy.can_edit(profile, translation):
            raise TranslationUpdateNotAllowed
        
        self.translation_repo.update_translation(
            translation, 
            {
                "name": data.name,
                "privacy_id": data.privacy
            }
        )

        return translation
    
    
    def user_delete_translation(self, profile, translation: Translation):
        if self.translation_policy.can_delete(profile, translation):
            self.translation_repo.delete_translation(translation)

        raise TranslationDeleteNotAllowed