from typing import Optional, List

from werkzeug.datastructures import FileStorage

from app import db

from .models import Translation, Manga
from .schemas import MangaFormSchema


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
    def create_manga(self, data: MangaFormSchema, posters: List[FileStorage], background: Optional[FileStorage]):
        pass

    def update_manga(self, data: MangaFormSchema, new_posters: List[FileStorage], background: Optional[FileStorage]):
        pass