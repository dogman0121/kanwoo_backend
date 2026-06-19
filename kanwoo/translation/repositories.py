from sqlalchemy import select, exists


from kanwoo.repositories import BaseRepository
from kanwoo.profile.models import Profile

from .models import Translation

class TranslationRepository(BaseRepository):

    def get_translation_by_id(self, translation_id):
        return self.db_session.execute(select(Translation).filter_by(id=translation_id)).scalar()

    def get_manga_translations(self, manga_id: int, official: bool = False):
        return self.db_session.execute(select(Translation).filter_by(manga_id=manga_id, is_official=official)).scalars().all()
    
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
        