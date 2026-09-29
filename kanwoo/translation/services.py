from typing import Optional

from kanwoo.database import DBTransaction
from kanwoo.manga.models import Manga
from kanwoo.profile.models import Profile
from kanwoo.chapter.services import ChapterService

from .permissions import TranslationPolicy
from .dto import TranslationUpdateDTO, TranslationCreateDTO, TranslationContextDTO, TranslationListContextDTO
from .models import Translation, TranslationSubscribtion
from .repositories import TranslationRepository
from .exceptions import (
    TranslationNotFoundException, 
    TranslationAlreadyExistsException, 
    TranslationUpdateNotAllowed,
    TranslationCreateNotAllowed,
    TranslationDeleteNotAllowed
)

class TranslationService:

    def __init__(
        self, 
        translation_repo: TranslationRepository,
        translation_policy: TranslationPolicy,
        db_transaction: DBTransaction
    ):
        self.translation_repo = translation_repo
        self.translation_policy = translation_policy
        self.db_transaction = db_transaction

    def user_get_translation_by_id(self, profile, translation_id):
        translation = self.translation_repo.get_translation_by_id(translation_id)

        if translation is None:
            raise TranslationNotFoundException
        
        return translation


    def user_get_translation_context(self, profile, translation):

        return TranslationContextDTO(
            viewer={
                "is_subscribed": self.translation_repo.check_translation_subscription(translation, profile)
            }
        )

        return TranslationListContextDTO(viewer=translations_context_dict)

    def user_get_manga_translations(self, profile, manga: Manga, official: Optional[bool] = None):
        if official is None:
            translations = self.translation_repo.get_manga_translations(manga.id, official=True)

            if len(translations) == 0:
                return self.translation_repo.get_manga_translations(manga.id, official=False)
            
            return translations
        else:
            return self.translation_repo.get_manga_translations(manga.id, official=official)
        
    def user_create_manga_translation(self, creator_profile, owner_profile, manga: Manga, data):
        if not self.translation_policy.can_create(creator_profile, owner_profile):
            raise TranslationCreateNotAllowed()
        if self.translation_repo.check_translation_with_same_lang(owner_profile.id, manga.id, data.lang_id):
            raise TranslationAlreadyExistsException()
        
        translation = Translation(
            name=data.name,
            lang_id=data.lang_id,
            manga_id=manga.id,
            privacy_id=data.privacy_id,
            owner_id=owner_profile.id,
            creator_id=creator_profile.id,
            is_official=data.is_official
        )
        
        return self.translation_repo.create_translation(translation)
    
    def user_get_profile_translations(self, viewer_profile: Profile, profile: Profile):
        return self.translation_repo.get_profile_translations(viewer_profile, profile)
    
    def user_update_translation(self, profile, translation: Translation, data: TranslationUpdateDTO):
        if not self.translation_policy.can_edit(profile, translation):
            raise TranslationUpdateNotAllowed()
        
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

    def user_subscribe_translation(self, profile: Profile, translation: Translation):
        if self.translation_repo.check_translation_subscription(profile, translation):
            return

        with self.db_transaction:
            translation_subscription = TranslationSubscribtion(
                profile_id=profile.id,
                translation_id=translation.id
            )

            self.translation_repo.create_translation_subscription(translation_subscription)

    def user_unsubscribe_translation(self, profile: Profile, translation: Translation):
        self.translation_repo.delete_translation_subscription(profile, translation)