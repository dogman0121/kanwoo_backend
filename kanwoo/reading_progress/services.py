from __future__ import annotations
from typing import List, TYPE_CHECKING

from kanwoo.exceptions import ApiNotFound

if TYPE_CHECKING:
    from kanwoo.database import DBTransaction
    from kanwoo.profile.models import Profile
    from kanwoo.manga.models import Manga
    from kanwoo.translation.models import Translation
    from kanwoo.chapter.models import Chapter
    from kanwoo.translation.services import MangaTranslationService

from kanwoo.profile.entity import AnonymousProfile

from .dto import (
    ReadingHistoryContextDTO, 
    ReadingBookmarkContextDTO,
    UpdateReadingSessionDTO,
    UpdateHistoryItemDTO,
    CreateHistoryItemDTO,
    ChapterProgressDTO,
    ReadingStartDTO
)
from .models import ReadingHistory, ReadingBookmark, ReadingSession
from .repositories import ReadingBookmarkRepository, ReadingHistoryRepository, ReadingSessionRepository
from .entities import ReadingStartTypeEnum

class ReadingBookmarkService:

    def __init__(
        self,
        reading_bookmark_repo: ReadingBookmarkRepository,
        db_transaction: DBTransaction
    ):
        self.rb_repo = reading_bookmark_repo
        self.db_transaction = db_transaction

    def get_reading_bookmark_by_id(self, actor: Profile, bookmark_id: int):
        bookmark = self.rb_repo.get_reading_bookmark_by_id(actor.id, bookmark_id)

        if bookmark is None:
            raise ApiNotFound(code="bookmark_not_found")

        return bookmark

    def get_reading_bookmarks(self, actor):
        return self.rb_repo.get_profile_reading_bookmarks(actor.id)

    def set_reading_bookmark(
        self, 
        actor: Profile, 
        manga: Manga, 
        translation: Translation, 
        chapter_number: int, 
        page_number: int
    ):
        with self.db_transaction:
            self.rb_repo.upsert_reading_bookmark(
                actor.id,
                manga.id,
                translation.id,
                chapter_number,
                page_number,
            )


    def delete_reading_bookmark(self, actor, bookmark_id: int):
        with self.db_transaction:
            self.rb_repo.delete_reading_bookmark(actor.id, bookmark_id)


class ReadingBookmarkContextService:

    def __init__(self):
        pass

    def get(
        self, 
        actor: Profile, 
        bookmark: ReadingBookmark,
        include_chapter = False,
        include_manga = False
    ):
        context = ReadingBookmarkContextDTO(
            chapter=None,
            manga=None
        )

        if include_chapter:
            context.chapter = bookmark.chapter
        if include_manga:
            context.manga = bookmark.manga

        return context

class ReadingHistoryService:

    def __init__(
        self, 
        reading_bookmark_service: ReadingBookmarkService,
        reading_history_repo: ReadingHistoryRepository,
        db_transaction: DBTransaction
    ):
        self.rh_repo = reading_history_repo
        self.db_transaction = db_transaction
        self.rb_service = reading_bookmark_service

    def user_get_history_by_id(self, actor: Profile, progress_id: int):
        return self.progress_repo.get_history_item_by_id(actor.id, progress_id)

    def system_create_history(self, create_dto: CreateHistoryItemDTO):
        with self.db_transaction:
            history_item = ReadingHistory(
                reading_session_id=create_dto.session_id,
                chapter_id=create_dto.chapter_id,
                page=create_dto.page,
            )

            self.rh_repo.create(history_item)

            return history_item

    def system_update_history(self, history_item: ReadingHistory, update_dto: UpdateHistoryItemDTO):
        
        with self.db_transaction:    
            self.rh_repo.update(
                history_item,
                {
                    "page": update_dto.page,
                }
            )

        return history_item
            
    def user_get_history(self, actor: Profile, cursor = None):
        history, cursor, has_more = self.rh_repo.get_reading_history(actor.id, cursor)

        return history, cursor, has_more

    def user_delete_selected_history(self, actor: Profile, history_ids: List[int]):
        self.rh_repo.delete_many_history(actor.id, history_ids)

    def user_delete_all_history(self, actor: Profile):
        self.rh_repo.delete_all_history(actor.id)

    def user_get_history_context(self, actor: Profile, history_item: ReadingHistory, include_chapter=False, include_manga=False, include_translation=False):
        context = ReadingHistoryContextDTO(
            chapter=None,
            manga=None,
            translation=None
        )

        if include_chapter:
            context.chapter = history_item.chapter
        if include_translation:
            context.translation = history_item.chapter.translation
        if include_manga:
            context.manga = history_item.chapter.translation.manga

        return context
    

class ReadingSessionService:

    def __init__(
        self,
        reading_session_repo: ReadingSessionRepository,
        reading_history_service: ReadingHistoryService,
        db_transaction: DBTransaction
    ):
        self.session_repo = reading_session_repo
        self.history_service = reading_history_service
        self.db_transaction = db_transaction

    def user_get_reading_session_by_id(self, actor: Profile, session_id: int):
        return self.session_repo.get_reading_session_by_id(actor.id, session_id)

    def user_get_reading_session(self, actor: Profile, translation):
        with self.db_transaction:
            reading_session = ReadingSession(
                profile_id=actor.id,
                translation_id=translation.id
            )

            self.session_repo.create_reading_session(reading_session)

        return reading_session

    def update_reading_session(self, actor: Profile, session: ReadingSession, update_dto: UpdateReadingSessionDTO):

        last_history_item = session.last_history_item

        with self.db_transaction:
            if last_history_item and last_history_item.chapter_id == update_dto.chapter_id:
                history_update_dto = UpdateHistoryItemDTO(
                    page = update_dto.page
                )

                self.history_service.system_update_history(last_history_item, history_update_dto)
            else:
                history_create_dto = CreateHistoryItemDTO(
                    chapter_id=update_dto.chapter_id,
                    session_id=session.id,
                    page=update_dto.page
                )

                self.history_service.system_create_history(history_create_dto)


class ReadingHistoryContextService:

    def __init__(self):
        pass

    def get(
        self, 
        actor: Profile, 
        history_item: ReadingHistory, 
        include_chapter=False, 
        include_manga=False, 
        include_translation=False
    ):
        context = ReadingHistoryContextDTO(
            chapter=None,
            manga=None,
            translation=None
        )

        if include_chapter:
            context.chapter = history_item.chapter
        if include_translation:
            context.translation = history_item.chapter.translation
        if include_manga:
            context.manga = history_item.chapter.translation.manga

        return context

class MangaReadingStartService:

    def __init__(
        self,
        reading_bookmark_repo: ReadingBookmarkRepository,
        manga_translation_service: MangaTranslationService
    ):
        self.bookmark_repo = reading_bookmark_repo
        self.manga_translation_service = manga_translation_service

    def _get_first_chapter_start(self, manga_slug: str) -> Chapter:
        most_recommended_translation = self.manga_translation_service.get(manga_slug, cnt=1)

        if len(most_recommended_translation) == 0:
            return ReadingStartDTO(
                start_type=ReadingStartTypeEnum.NO_CHAPTER,
                chapter=None
            )

        first_chapter = most_recommended_translation[0].first_chapter
        if first_chapter is None:
            return ReadingStartDTO(
                start_type=ReadingStartTypeEnum.NO_CHAPTER,
                chapter=None
            )

        return ReadingStartDTO(
            start_type=ReadingStartTypeEnum.START,
            chapter=first_chapter
        )

    def get(self, actor, manga):
        if isinstance(actor, AnonymousProfile):
            return self._get_first_chapter_start(manga.slug)

        bookmark = self.bookmark_repo.get_manga_reading_bookmark(actor.id, manga.id)

        if bookmark is None or bookmark.chapter is None:
            return self._get_first_chapter_start(manga.slug)

        return ReadingStartDTO(
            start_type=ReadingStartTypeEnum.CONTINUE,
            chapter=bookmark.chapter
        )

class ChapterProgressService:

    def __init__(
        self,
        reading_history_repo: ReadingHistoryRepository
    ):
        self.history_repo = reading_history_repo

    def get(self, actor, chapter_id) -> ChapterProgressDTO:
        progress: ReadingHistory = self.history_repo.get_chapter_progress(actor.id, chapter_id)

        if progress is None or progress.is_finished:
            return ChapterProgressDTO(
                page=0
            )

        return ChapterProgressDTO(
            page=progress.page
        )

