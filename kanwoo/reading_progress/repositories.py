from sqlalchemy import select, func, delete, desc, Date, or_, and_, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import aliased, joinedload, contains_eager

from kanwoo.repositories import BaseRepository
from kanwoo.models import cursor_paginate
from kanwoo.manga.models import Manga
from kanwoo.chapter.models import Chapter
from kanwoo.translation.models import Translation

from .models import ReadingProgress, ReadingSave

class ReadingProgressRepository(BaseRepository):

    def get_progress_by_id(self, actor_id, progress_id):
        return self.db_session.execute(
            select(ReadingProgress).filter(
                ReadingProgress.id == progress_id, 
                ReadingProgress.profile_id == actor_id
            )
        ).scalar()
    
    def get_manga_progress(self, profile_id, manga_id):
        return self.db_session.execute(
            select(ReadingSave)
            .filter(
                ReadingSave.manga_id == manga_id, 
                ReadingSave.profile_id == profile_id
            )
        ).scalar_one_or_none()

    def get_chapter_progress(self, profile_id, chapter_id):
        return self.db_session.execute(
            select(ReadingProgress)
            .filter(
                ReadingProgress.chapter_id == chapter_id, 
                ReadingProgress.profile_id == profile_id
            )
            .order_by(ReadingProgress.created_at.desc())
            .limit(1)
        ).scalar()
    
    def delete_manga_progress(self, profile, manga_id):
        subq = (select(ReadingProgress.chapter_id)
            .join(Chapter, Chapter.id == ReadingProgress.chapter_id)
            .join(Translation, Translation.id == Chapter.translation_id)
            .where(Translation.manga_id==manga_id, ReadingProgress.profile_id == profile.id)
        ).subquery()

        self.db_session.execute(
            delete(ReadingProgress)
            .where(ReadingProgress.chapter_id.in_(select(subq)))
        )

    def get_reading_history(self, actor_id, cursor=None):
        rn = func.row_number().over(
            partition_by=(func.cast(ReadingProgress.created_at, Date), ReadingProgress.chapter_id),
            order_by=desc(ReadingProgress.created_at),
        ).label("rn")

        subq = (
            select(ReadingProgress, rn)
            .where(ReadingProgress.profile_id == actor_id)
            .subquery()
        )

        rp = aliased(ReadingProgress, subq)
        q = select(rp).filter(subq.c.rn == 1, subq.c.is_deleted == False)

        progresses, cursor, has_more = cursor_paginate(rp, self.db_session, q, cursor=cursor, direction="desc")

        return progresses, cursor, has_more

    def delete_all_progresses(self, profile_id):
        self.db_session.execute(delete(ReadingProgress).filter(ReadingProgress.profile_id == profile_id))

    def delete_many_progresses(self, profile_id, progresses_ids):
        self.db_session.execute(delete(ReadingProgress).filter(
            ReadingProgress.profile_id == profile_id, 
            ReadingProgress.id.in_(progresses_ids)
        ))

class ReadingSaveRepository(BaseRepository):

    def get_profile_progress(self, profile_id):
        query = (
            select(ReadingSave)
            .join(ReadingSave.chapter) 
            .filter(
                ReadingSave.profile_id == profile_id,
                or_(
                    ReadingSave.is_finished == False,
                    Chapter.is_last == False
                )
            )
            .order_by(ReadingSave.updated_at.desc())
            .options(
                contains_eager(ReadingSave.chapter)
                .joinedload(Chapter.next_chapter), 
                
                joinedload(ReadingSave.manga)
            )
        )
        
        return self.db_session.execute(query).scalars().all()

    def upsert_save(self, profile_id, manga_id, chapter_id, page, is_finished):
        insert_stmt = insert(ReadingSave).values(
            manga_id=manga_id, 
            chapter_id=chapter_id, 
            page=page, 
            profile_id=profile_id,
            is_finished=is_finished
        )

        update_stmt = insert_stmt.on_conflict_do_update(
            constraint="uq_reading_save_progress",
            set_={"chapter_id": chapter_id, "page": page, "is_finished": is_finished}
        )

        self.db_session.execute(update_stmt)

    def set_reading_is_finished(self, profile_id, chapter_id, is_finished):
        self.db_session.execute(
            update(ReadingSave)
            .values(
                is_finished=is_finished
            )
            .filter(
                ReadingSave.profile_id == profile_id, 
                ReadingSave.chapter_id == chapter_id
            )
        )

    def delete_save(self, profile_id, save_id):
        self.db_session.execute(
            delete(ReadingSave)
            .filter(
                ReadingSave.profile_id == profile_id,
                ReadingSave.id == save_id
            )
        )

    def delete_all_saves(self, profile_id):
        self.db_session.execute(
            delete(ReadingSave)
            .filter(
                ReadingSave.profile_id == profile_id,
            )
        )