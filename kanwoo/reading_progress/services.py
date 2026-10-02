from kanwoo.database import DBTransaction
from kanwoo.exceptions import ApiNotFound

from .dto import ReadingProgressContextDTO
from .exceptions import ReadingProgressNotFound
from .models import ReadingProgress
from .repositories import ReadingProgressRepository, ReadingSaveRepository


class ReadingProgressService:

    def __init__(
        self, 
        progress_repo: ReadingProgressRepository,
        save_repo: ReadingSaveRepository,
        db_transaction: DBTransaction
    ):
        self.progress_repo = progress_repo
        self.save_repo = save_repo
        self.db_transaction = db_transaction

    def user_get_progress_by_id(self, actor, progress_id):
        return self.progress_repo.get_progress_by_id(actor, progress_id)

    def user_create_progress(self, actor, create_dto):
        with self.db_transaction:
            progress = ReadingProgress(
                chapter_id=create_dto.chapter.id,
                page=create_dto.page or 0,
                profile_id=actor.id 
            )

            manga_id = create_dto.chapter.translation.manga_id

            progress.add(progress)
            self.save_repo.upsert_save(actor, manga_id, create_dto.chapter.id, 0)

            return progress

    def user_update_progress(self, actor, progress, update_dto):
        with self.db_transaction:
            progress.update({
                "page": update_dto.page
            })

            if progress.chapter.pages_count == update_dto.page + 1:
                self.save_repo.finish_reading(actor, progress.chapter)
            else:
                self.save_repo.upsert_save(actor, progress.chapter.translation.manga.id, progress.chapter_id, update_dto.page)

    def user_get_progresses(self, actor):
        return self.save_repo.get_profile_progress(actor)

    def user_get_manga_progress(self, actor, manga_slug):
        reading_progress = self.progress_repo.get_manga_progress(actor, manga_slug)

        if reading_progress is None:
            raise ReadingProgressNotFound()

        return reading_progress

    def user_get_chapter_progress(self, actor, chapter_id):
        progress = self.progress_repo.get_chapter_progress(actor, chapter_id)

        if progress is None:
            raise ApiNotFound()

        return progress
    
    def user_delete_progress(self, profile, progress):
        with self.db_transaction:
            self.progress_repo.update(progress, {
                "is_deleted": True
            })

    def user_delete_many_progresses(self, actor, progresses_ids):
        self.progress_repo.delete_manga_progresses(actor, progresses_ids)

    def user_delete_all_progresses(self, actor):
        self.progress_repo.delete_all_progresses(actor)

    def user_get_progress_context(self, actor, progress, include_chapter=False, include_manga=False, include_translation=False):
        context = ReadingProgressContextDTO(
            chapter=None,
            manga=None,
            translation=None
        )

        if include_chapter:
            context.chapter = progress.chapter
        if include_translation:
            context.translation = progress.translation
        if include_manga:
            context.manga = progress.manga

        return context


    def user_get_history(self, actor, cursor):
        return self.progress_repo.get_reading_history(actor, cursor)

    