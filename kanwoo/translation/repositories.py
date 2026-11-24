from sqlalchemy import select, exists, desc, delete
from typing import Optional

from kanwoo.manga.models import Manga
from kanwoo.repositories import BaseRepository
from kanwoo.profile.models import Profile
from kanwoo.entities import Privacy

from .models import Translation, TranslationSubscribtion

class TranslationRepository(BaseRepository):

    def get_translation_by_id(self, translation_id):
        return self.db_session.execute(select(Translation).filter_by(id=translation_id)).scalar()

    def get_manga_translations(
        self, 
        manga_slug: str, 
        official: Optional[bool] = None, 
        public: bool = True,
        cnt: Optional[int] = None
    ):
        stmt = (
            select(Translation)
            .join(Manga, Manga.id == Translation.manga_id)
            .where(
                Manga.slug == manga_slug,
            )
            .order_by(desc(Translation.chapters_count))
        )

        if official is not None:
            stmt = stmt.where(Translation.is_official == official)
        if public:
            stmt = stmt.where(Translation.privacy_id == Privacy.PUBLIC.value)
        if cnt is not None:
            stmt = stmt.limit(cnt)

        return self.db_session.execute(stmt).unique().scalars().all()
    
    def create_translation(self, translation: Translation):
        translation.add(commit=True)

        return translation
    
    def check_translation_with_same_lang(self, owner_id: int, manga_id: int, lang_id: int):
        return self.db_session.scalar(select(exists(Translation).where(
            Translation.owner_id==owner_id, 
            Translation.manga_id==manga_id, 
            Translation.lang_id==lang_id
        )))
    
    def get_profile_translations(self, viewer_profile, profile: Profile, official: bool = False):
        return self.db_session.execute(
            select(Translation).filter(
                Translation.owner_id==profile.id, 
                Translation.is_official==official,
                Translation.can_view(viewer_profile)
            )
        ).scalars().all()
    
    def update_translation(self, translation, data):
        translation.update(data, commit=True)

        return translation
    
    def delete_translation(self, translation: Translation):
        translation.delete(commit=True)

    def check_translation_subscription(self, profile: Profile, translation: Translation):
        return self.db_session.execute(
            select(
                exists(TranslationSubscribtion)
                .where(
                    TranslationSubscribtion.translation_id==translation.id,
                    TranslationSubscribtion.profile_id==profile.id
                )
            )
        ).scalar()

    def create_translation_subscription(self, translation_subscription: TranslationSubscribtion):
        translation_subscription.add()

    def delete_translation_subscription(self, profile: Profile, translation: Translation):
        return self.db_session.execute(
            delete(TranslationSubscribtion)
            .where(
                TranslationSubscribtion.profile_id == profile.id,
                TranslationSubscribtion.translation_id == translation.id
            )
        )