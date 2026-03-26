from abc import abstractmethod, ABC

from sqlalchemy import func, select

from kanwoo.repositories import BaseRepository

from .models import MangaModerationStatus, ChapterModerationStatus

class ModerationRepository(BaseRepository, ABC):

    @abstractmethod
    def get_waiting_moderation_count(self):
        pass

    @abstractmethod
    def add_moderation_status(self, moderation_status):
        pass

class MangaModerationRepository(ModerationRepository):

    def get_waiting_moderation_count(self):
        subq = select(MangaModerationStatus.status_type_id, func.row_number().over(
            partition_by=MangaModerationStatus.manga_id,
            order_by=MangaModerationStatus.created_at.desc()
        ).label("rn")).subquery()

        return self.db_session.execute(
            select(func.count("*")).select_from(subq)
            .where(
                subq.c.rn == 1,
                subq.c.status_type_id == 1
            )
        ).scalar()
    
    def add_moderation_status(self, moderation_status):
        print(123)
        moderation_status.add(commit=True)

        return moderation_status
    
class ChapterModerationRepository(ModerationRepository):

    def get_waiting_moderation_count(self):
        subq = select(ChapterModerationStatus.status_type_id, func.row_number().over(
            partition_by=ChapterModerationStatus.manga_id,
            order_by=ChapterModerationStatus.created_at.desc()
        ).label("rn")).subquery()

        return self.db_session.execute(
            select(func.count("*")).select_from(subq)
            .where(
                subq.c.rn == 1,
                subq.c.status_type_id == 1
            )
        ).scalar()
    
    def add_moderation_status(self, moderation_status):
        pass