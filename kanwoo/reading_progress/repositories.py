from sqlalchemy import exists, and_, select, func, delete
from sqlalchemy.orm import aliased


from kanwoo import db
from kanwoo.repositories import BaseRepository
from kanwoo.chapter.models import Chapter
from kanwoo.translation.models import Translation

from .models import ReadingProgress

class ReadingProgressRepository(BaseRepository):

    def check_chapter_progress(self, chapter):
        return self.db_session.execute(
            exists(ReadingProgress.chapter_id).where(
                and_(
                    ReadingProgress.chapter_id == chapter.id, 
                    ReadingProgress.profile_id == self.profile.id
                )
            )
        ).scalar()
    
    def get_chapter_progress(self, chapter):
        return self.db_session.execute(select(ReadingProgress).filter_by(profile_id=self.profile.id, chapter_id=chapter.id)).scalar()
    
    def get_manga_progress(self, manga_id, profile_id):
        return self.db_session.execute(
            select(ReadingProgress)
            .filter(
                ReadingProgress.profile_id == profile_id,
                ReadingProgress.manga_id == manga_id)
            .order_by(ReadingProgress.updated_at.desc())
        ).scalar()
    
    def get_profile_progress(self, profile_id):
        subq = (
            select(
                ReadingProgress,
                func.row_number().over(
                    partition_by=ReadingProgress.manga_id,
                    order_by=ReadingProgress.updated_at.desc()
                ).label("row_number")
            )
            .join(ReadingProgress.chapter)
            .join(ReadingProgress.translation)
            .where(
                ReadingProgress.profile_id == profile_id,
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
        )

        return self.db_session.execute(stmt).scalars().all()
    
    def get_chapter_progress(self, profile_id, chapter_id):
        return self.db_session.execute(select(ReadingProgress).filter_by(chapter_id=chapter_id, profile_id=profile_id)).scalar()
    
    def update_progress(self, reading_progress, data: dict):
        return reading_progress.update(data, commit=True)
    
    def delete_manga_progress(self, manga_id, profile_id):
        subq = (select(ReadingProgress.chapter_id)
            .join(Chapter, Chapter.id == ReadingProgress.chapter_id)
            .join(Translation, Translation.id == Chapter.translation_id)
            .where(Translation.manga_id==manga_id, ReadingProgress.profile_id == profile_id)
        ).subquery()

        self.db_session.execute(
            delete(ReadingProgress)
            .where(ReadingProgress.chapter_id.in_(select(subq)))
        )

    def create_progress(self, reading_progress):
        reading_progress.add(commit=True)

        return reading_progress
    
    def get_progress_by_id(self, profile, progress_id):
        return self.db_session.execute(
            select(ReadingProgress).filter(ReadingProgress.id == progress_id)
        ).scalar()