from sqlalchemy import select, func, delete, desc, Date, or_, and_, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import aliased, joinedload, contains_eager

from kanwoo.repositories import BaseRepository
from kanwoo.models import cursor_paginate
from kanwoo.manga.models import Manga
from kanwoo.chapter.models import Chapter
from kanwoo.translation.models import Translation

from .models import ReadingBookmark, ReadingHistory, ReadingSession

class ReadingHistoryRepository(BaseRepository):

    def get_history_item_by_id(self, actor_id, progress_id):
        return self.db_session.execute(
            select(ReadingHistory).filter(
                ReadingHistory.id == progress_id, 
                ReadingHistory.profile_id == actor_id
            )
        ).scalar()

    def get_reading_history(self, actor_id, cursor=None):
        stmt = (
            select(ReadingHistory)
            .join(ReadingSession, ReadingHistory.reading_session_id == ReadingSession.id)
            .where(ReadingSession.profile_id == actor_id)
        )

        progresses, cursor, has_more = cursor_paginate(ReadingHistory, self.db_session, stmt, cursor=cursor, direction="desc")

        return progresses, cursor, has_more

    def delete_all_history(self, profile_id):
        self.db_session.execute(delete(ReadingHistory).filter(ReadingHistory.profile_id == profile_id))

    def delete_many_history(self, profile_id, progresses_ids):
        self.db_session.execute(delete(ReadingHistory).filter(
            ReadingHistory.profile_id == profile_id, 
            ReadingHistory.id.in_(progresses_ids)
        ))

    def get_chapter_progress(self, profile_id, chapter_id):
        stmt = (
            select(ReadingHistory)
            .join(ReadingSession, ReadingHistory.reading_session_id == ReadingSession.id)
            .where(
                ReadingSession.profile_id == profile_id,
                ReadingHistory.chapter_id == chapter_id,
                ReadingHistory.is_finished == False
            )
            .order_by(ReadingHistory.updated_at.desc())
            .limit(1)
        )
        return self.db_session.execute(stmt).scalar_one_or_none()

class ReadingBookmarkRepository(BaseRepository):

    def get_reading_bookmark_by_id(self, profile_id, bookmark_id):
        return self.db_session.execute(
            select(ReadingBookmark)
            .filter(
                ReadingBookmark.profile_id == profile_id,
                ReadingBookmark.id == bookmark_id
            )
        ).scalar()

    def get_profile_reading_bookmarks(self, profile_id):
        query = (
            select(ReadingBookmark)
            .filter(
                ReadingBookmark.profile_id == profile_id,
                ReadingBookmark.chapter.has()
            )
            .order_by(ReadingBookmark.updated_at.desc())
        )
        
        return self.db_session.execute(query).scalars().all()

    def upsert_reading_bookmark(self, profile_id, manga_id, translation_id, chapter_id, page):
        insert_stmt = insert(ReadingBookmark).values(
            manga_id=manga_id, 
            translation_id=translation_id,
            chapter_number=chapter_id, 
            page_number=page, 
            profile_id=profile_id,
        )

        update_stmt = insert_stmt.on_conflict_do_update(
            constraint="uq_reading_bookmark",
            set_={"translation_id": translation_id, "chapter_number": chapter_id, "page_number": page}
        )

        self.db_session.execute(update_stmt)

    def set_reading_bookmark_is_finished(self, profile_id, chapter_id, is_finished):
        self.db_session.execute(
            update(ReadingBookmark)
            .values(
                is_finished=is_finished
            )
            .filter(
                ReadingBookmark.profile_id == profile_id, 
                ReadingBookmark.chapter_id == chapter_id
            )
        )

    def delete_reading_bookmark(self, profile_id, bookmark_id):
        self.db_session.execute(
            delete(ReadingBookmark)
            .filter(
                ReadingBookmark.profile_id == profile_id,
                ReadingBookmark.id == bookmark_id
            )
        )

    def delete_all_reading_bookmarks(self, profile_id):
        self.db_session.execute(
            delete(ReadingBookmark)
            .filter(
                ReadingBookmark.profile_id == profile_id,
            )
        )

    def get_manga_reading_bookmark(self, profile_id, manga_id):
        return self.db_session.execute(
            select(ReadingBookmark)
            .filter(
                ReadingBookmark.profile_id == profile_id,
                ReadingBookmark.manga_id == manga_id
            )
        ).scalar()

    def get_chapter_reading_bookmark(self, profile_id, chapter_id):
        self.db_session.execute(
            select(ReadingBookmark)
            .filter(
                ReadingBookmark.profile_id == profile_id,
                ReadingBookmark.chapter_id == chapter_id
            )
        ).scalar()

class ReadingSessionRepository(BaseRepository):

    def get_reading_session_by_id(self, actor_id, session_id):
        return self.db_session.execute(
            select(ReadingSession)
            .filter(
                ReadingSession.profile_id==actor_id,
                ReadingSession.id == session_id
            )
        ).scalar_one_or_none()

    def create_reading_session(self, reading_session):
        self.create(reading_session)