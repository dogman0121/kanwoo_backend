from datetime import datetime

from kanwoo.database import DBTransaction

from .dto import ReadingProgressDTO
from .exceptions import ReadingProgressNotFound
from .models import ReadingProgress
from .repositories import ReadingProgressRepository


class ReadingProgressService:

    def __init__(
        self, 
        reading_progress_repo: ReadingProgressRepository,
        db_transaction: DBTransaction
    ):
        self.reading_progress_repo = reading_progress_repo
        self.db_transaction = db_transaction

    def user_get_progress_by_id(self, profile, progress_id):
        return self.reading_progress_repo.get_progress_by_id(profile, progress_id)

    def user_get_manga_progress(self, profile, manga):
        reading_progress = self.reading_progress_repo.get_manga_progress(manga.id, profile.id)

        if reading_progress is None:
            raise ReadingProgressNotFound

        return reading_progress

    def user_get_profile_progresses(self, profile):
        return self.reading_progress_repo.get_profile_progress(profile.id)

    def user_update_manga_reading_progress(self, profile, manga, chapter, progress: ReadingProgressDTO):
        
        reading_progress = ReadingProgress(
            manga_id=manga.id,
            translation_id=chapter.translation_id,
            profile_id=profile.id,
            chapter_id=progress.chapter_id,
            page=progress.page
        )

        return self.reading_progress_repo.create_progress(reading_progress)

    def user_delete_manga_reading_progress(self, profile, manga):
        return self.reading_progress_repo.delete_manga_progress(manga.id, profile.id)
    
    def user_update_chapter_progress(self, profile, chapter, progress_data: ReadingProgressDTO):
        with self.db_transaction:
            return self.reading_progress_repo.create_progress(
                ReadingProgress(
                    manga_id = chapter.translation.manga_id,
                    translation_id = chapter.translation_id,
                    chapter_id = chapter.id,
                    profile_id = profile.id,
                    page = progress_data.page
                )
            )
    
    def user_delete_progress(self, profile, progress):
        pass

    def user_get_chapter_progress(self, profile, chapter):
        return self.reading_progress_repo.get_chapter_progress(profile.id, chapter.id)
    
    def user_delete_progress(self, profile, progress):
        with self.db_transaction:
            progress.update({
                "is_deleted": True
            })
        
