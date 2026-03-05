from datetime import datetime

from .dto import ReadingProgressDTO
from .exceptions import ReadingProgressNotFound
from .models import ReadingProgress
from .repositories import ReadingProgressRepository

class ReadingProgressService:

    def __init__(self, reading_progress_repo: ReadingProgressRepository):
        self.reading_progress_repo = reading_progress_repo

    def user_get_manga_progress(self, profile, manga):
        reading_progress = self.reading_progress_repo.get_manga_progress(manga.id, profile.id)

        if reading_progress is None:
            raise ReadingProgressNotFound

        return reading_progress

    def user_get_profile_progress(self, profile):
        return self.reading_progress_repo.get_profile_progress(profile.id)

    def user_update_manga_reading_progress(self, profile, manga, progress: ReadingProgressDTO):
        reading_progress = self.reading_progress_repo.get_manga_progress(manga.id, profile.id)
        if not reading_progress:
            reading_progress = ReadingProgress(
                manga_id=manga.id,
                profile_id=profile.id,
                chapter_id=progress.chapter_id,
                page=progress.page
            )

            return self.reading_progress_repo.create_progress(reading_progress)

        return self.reading_progress_repo.update_progress(reading_progress, {
            "chapter_id": progress.chapter_id,
            "page": progress.chapter_id
        })

    def user_delete_manga_reading_progress(self, profile, manga):
        return self.reading_progress_repo.delete_manga_progress(manga.id, profile.id)
    
    def user_update_chapter_progress(self, profile, chapter, progress_data: ReadingProgressDTO):
        progress = self.reading_progress_repo.get_chapter_progress(profile.id, chapter.id)
        if progress:
            return self.reading_progress_repo.update_progress(
                progress,
                {
                    "page": progress_data.page,
                    "updated_at": datetime.now()
                }
            )
        
        return self.reading_progress_repo.create_progress(
            ReadingProgress(
                chapter_id = chapter.id,
                profile_id = profile.id,
                page = progress_data.page
            )
        )

    def user_get_chapter_progress(self, profile, chapter):
        return self.reading_progress_repo.get_chapter_progress(profile.id, chapter.id)
        
