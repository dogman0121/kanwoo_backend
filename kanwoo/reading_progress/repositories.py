from sqlalchemy import select, func, delete, desc, Date, or_, and_, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import aliased

from kanwoo.repositories import BaseRepository
from kanwoo.models import cursor_paginate
from kanwoo.manga.models import Manga
from kanwoo.chapter.models import Chapter
from kanwoo.translation.models import Translation

from .models import ReadingProgress, ReadingSave
from .entities import ReadingSaveEnum

class ReadingProgressRepository(BaseRepository):

    def get_progress_by_id(self, actor, progress_id):
        return self.db_session.execute(
            select(ReadingProgress).filter(
                ReadingProgress.id == progress_id, 
                ReadingProgress.profile_id == actor.id
            )
        ).scalar()
    
    def get_manga_progress(self, profile, manga_slug):
        return self.db_session.execute(
            select(ReadingProgress).select_from(
                select(Manga)
                .join(Translation, Translation.manga_id == Manga.id)
                .join(Chapter, Chapter.translation_id == Translation.id)
                .join(ReadingProgress, ReadingProgress.chapter_id == Translation.id)
                .filter(Manga.slug == manga_slug)
            )
            .filter(ReadingProgress.profile_id == profile.id)
            .order_by(desc(ReadingProgress.created_at))
            .limit(1)
        ).scalar_one_or_none()

    def get_chapter_progress(self, profile, chapter_id):
        return self.db_session.execute(
            select(ReadingProgress)
            .filter(
                ReadingProgress.chapter_id == chapter_id, 
                ReadingProgress.profile_id == profile.id
            )
            .order_by(ReadingProgress.created_at.desc())
            .limit(1)
        ).scalar()
    
    def get_profile_progress(self, profile):
        subq = (
            select(
                ReadingProgress,
                func.row_number().over(
                    partition_by=Manga.id,
                    order_by=ReadingProgress.created_at.desc()
                ).label("rn")
            )
            .join(Chapter, ReadingProgress.chapter_id == Chapter.id)
            .join(Translation, Chapter.translation_id == Translation.id)
            .join(Manga, Translation.manga_id == Manga.id)
            .where(
                ReadingProgress.profile_id == profile.id,
                Chapter.chapter != Translation.chapters_count
            )
            .subquery()
        )

        rp_alias = aliased(ReadingProgress, subq)

        stmt = (
            select(rp_alias)
            .where(
                subq.c.row_number == 1,
                rp_alias.is_deleted != True
            )
            .order_by(rp_alias.created_at.desc())
        )

        return self.db_session.execute(stmt).scalars().all()
    
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

    def get_reading_history(self, actor, cursor=None):
        rn = func.row_number().over(
            partition_by=(func.cast(ReadingProgress.created_at, Date), ReadingProgress.chapter_id),
            order_by=desc(ReadingProgress.created_at),
        ).label("rn")

        subq = (
            select(ReadingProgress, rn)
            .where(ReadingProgress.profile_id == actor.id)
            .subquery()
        )

        rp = aliased(ReadingProgress, subq)
        q = select(rp).filter(subq.c.rn == 1, subq.c.is_deleted == False)

        progresses, cursor, has_more = cursor_paginate(rp, self.db_session, q, cursor=cursor, direction="desc")

        return progresses, cursor, has_more

    def delete_all_progresses(self, profile):
        self.db_session.execute(delete(ReadingProgress).filter(ReadingProgress.profile_id == profile.id))

    def delete_many_progresses(self, profile, progresses_ids):
        self.db_session.execute(delete(ReadingProgress).filter(
            ReadingProgress.profile_id == profile.id, 
            ReadingProgress.id.in_(progresses_ids)
        ))

class ReadingSaveRepository(BaseRepository):

    def get_profile_progress(self, profile):
        res = self.db_session.execute(
            select(ReadingSave)
            .join(Chapter, ReadingSave.chapter_id == Chapter.id)
            .join(Translation, Chapter.translation_id == Translation.id)
            .filter(
                ReadingSave.profile_id == profile.id,
                and_(ReadingSave.status_type_id != ReadingSaveEnum.FINISHED.value, Chapter.id != Translation.last_chapter_id)
            )
            .order_by(ReadingSave.updated_at.desc())
        ).scalars().all()

        return res

    def upsert_save(self, profile, manga_id, chapter_id, page):
        insert_stmt = insert(ReadingSave).values(
            manga_id=manga_id, 
            chapter_id=chapter_id, 
            page=page, 
            status_type_id=1,
            profile_id=profile.id
        )

        update_stmt = insert_stmt.on_conflict_do_update(
            constraint="uq_reading_save_progress",
            set_={"chapter_id": chapter_id, "page": page}
        )

        self.db_session.execute(update_stmt)

    def finish_reading(self, profile, chapter):
        if chapter.is_last:
            self.db_session.execute(
                update(ReadingSave)
                .values(
                    status_type_id = ReadingSaveEnum.FINISHED.value
                )
                .filter(ReadingSave.profile_id == profile.id, ReadingSave.chapter_id == chapter.id)
            )
        else:
            self.db_session.execute(
                update(ReadingSave)
                .values(
                    chapter_id = chapter.next_chapter.id,
                    status_type_id = ReadingSaveEnum.NOT_STARTED.value
                )
                .filter(ReadingSave.profile_id == profile.id, ReadingSave.chapter_id == chapter.id)
            )