from abc import abstractmethod, ABC
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from kanwoo.repositories import BaseRepository

from .models import MangaReport, ChapterReport


class ReportRepository(ABC, BaseRepository):

    @abstractmethod
    def create_report(self, report):
        pass
    
    @abstractmethod
    def update_report(self, report, data):
        pass

    @abstractmethod
    def get_waiting_moderation_count(self):
        pass

    @abstractmethod
    def get_all_reports(self, resolved = None):
        pass

    @abstractmethod
    def get_report_by_id(self, report_id):
        pass


class MangaReportRepository(ReportRepository):

    def create_report(self, report):
        report.add(commit=True)

        return report
    
    def update_report(self, report, data):
        report.update(data, commit=True)

    def get_waiting_moderation_count(self):
        return self.db_session.execute(
            select(func.count("*"))
            .where(MangaReport.resolved_at == None)
        ).scalar()
    
    def get_all_reports(self, resolved=None):
        q = select(MangaReport).options(joinedload(MangaReport.manga))

        if resolved is None:
            pass
        else:
            if resolved:
                q = q.filter(MangaReport.resolved_at.isnot(None))
            else:
                q = q.filter(MangaReport.resolved_at.is_(None))

        return self.db_session.execute(q.order_by(MangaReport.created_at)).scalars().all()
    
    def get_report_by_id(self, report_id):
        return self.db_session.execute(
            select(MangaReport)
            .options(joinedload(MangaReport.manga))
            .filter(MangaReport.id == report_id)
        ).scalar()

class ChapterReportRepository(ReportRepository):

    def create_report(self, report):
        report.add(commit=True)

        return report
    
    def update_report(self, report, data):
        report.update(data, commit=True)

    def get_waiting_moderation_count(self):
        return self.db_session.execute(
            select(func.count("*"))
            .where(ChapterReport.resolved_at == None)
        ).scalar()
        
    def get_all_reports(self, resolved=None):
        q = select(ChapterReport).options(joinedload(ChapterReport.chapter))

        if resolved is None:
            pass
        else:
            if resolved:
                q = q.filter(ChapterReport.resolved_at.isnot(None))
            else:
                q = q.filter(ChapterReport.resolved_at.is_(None))

        return self.db_session.execute(q.order_by(ChapterReport.created_at)).scalars().all()
    
    def get_report_by_id(self, report_id):
        return self.db_session.execute(
            select(ChapterReport)
            .options(joinedload(ChapterReport.chapter))
            .filter(ChapterReport.id == report_id)
        ).scalar()