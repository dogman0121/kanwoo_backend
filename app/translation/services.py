from app.manga.models import Manga

from .models import Translation
from .exceptions import TranslationNotFoundException, TranslationAlreadyExistsException

class TranslationService:
    def __init__(self, profile):
        self.profile = profile

    @staticmethod
    def get_translation_by_id(translation_id):
        translation = Translation.query.filter_by(id=translation_id).scalar()

        if translation is None:
            raise TranslationNotFoundException
        
        return translation

    def add_translation(self):
        pass

    def create_manga_translation(self, manga: Manga):
        try:
            self.get_manga_translation(manga)

            raise TranslationAlreadyExistsException
        except TranslationNotFoundException:
            pass
            

        translation = Translation(
            creator_id = self.profile.id,
            manga_id = manga.id
        )

        translation.add()

        return translation

    def get_manga_translation(self, manga: Manga):
        translation = Translation.query.filter_by(manga_id = manga.id).scalar()

        if translation is None:
            raise TranslationNotFoundException
        return translation
    
