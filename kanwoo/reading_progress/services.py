from kanwoo.database import DBTransaction
from kanwoo.exceptions import ApiNotFound

from .dto import ReadingProgressContextDTO, ReadingSaveDTO
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
        return self.progress_repo.get_progress_by_id(actor.id, progress_id)

    def user_create_progress(self, actor, create_dto):
        with self.db_transaction:
            progress = ReadingProgress(
                chapter_id=create_dto.chapter.id,
                page=create_dto.page or 0,
                profile_id=actor.id 
            )

            manga_id = create_dto.chapter.translation.manga_id

            progress.add(progress)
            self.save_repo.upsert_save(
                actor.id, 
                manga_id, 
                create_dto.chapter.id, 
                create_dto.page or 0, 
                False
            )

            return progress

    def user_update_progress(self, actor, progress, update_dto):
        
        with self.db_transaction:    
            is_last_page = progress.chapter.pages_count == update_dto.page + 1

            progress.update({
                "page": update_dto.page,
            })

            manga_id = progress.chapter.manga.id

            self.save_repo.upsert_save(
                actor.id,
                manga_id,
                progress.chapter_id,
                update_dto.page,
                is_last_page
            )

    def user_get_progresses(self, actor):
        progresses = self.save_repo.get_profile_progress(actor.id)

        prepared_saves = []
        for p in progresses:
            save = ReadingSaveDTO(
                id=p.id,
                chapter=p.chapter,
                manga=p.manga,
                page=p.page,
                is_finished=p.is_finished
            )

            if save.is_finished:
                if save.chapter.next_chapter is None:
                    raise KeyError("Can't get next chapter")
                
                save.is_finished = False
                save.page = 0
                save.chapter = save.chapter.next_chapter
                
            prepared_saves.append(save)

        return prepared_saves

    def user_get_manga_progress(self, actor, manga_id):
        reading_progress = self.progress_repo.get_manga_progress(actor.id, manga_id)

        if reading_progress is None:
            raise ReadingProgressNotFound()

        return reading_progress

    def user_get_chapter_progress(self, actor, chapter_id):
        progress = self.progress_repo.get_chapter_progress(actor.id, chapter_id)

        if progress is None:
            raise ApiNotFound()

        return progress
    
    def user_delete_progress_save(self, profile, save_id):
        with self.db_transaction:
            self.save_repo.delete_save(profile.id, save_id)
            
    def user_delete_all_progress_saves(self, profile):
        with self.db_transaction:
            self.save_repo.delete_all_saves(profile.id)

    def user_delete_many_progresses(self, actor, progresses_ids):
        self.progress_repo.delete_many_progresses(actor.id, progresses_ids)

    def user_delete_all_progresses(self, actor):
        self.progress_repo.delete_all_progresses(actor.id)

    def user_get_progress_context(self, actor, progress, include_chapter=False, include_manga=False, include_translation=False):
        context = ReadingProgressContextDTO(
            chapter=None,
            manga=None,
            translation=None
        )

        if include_chapter:
            context.chapter = progress.chapter
        if include_translation:
            context.translation = progress.chapter.translation
        if include_manga:
            context.manga = progress.chapter.translation.manga

        return context


    def user_get_history(self, actor, cursor):
        return self.progress_repo.get_reading_history(actor.id, cursor)

    