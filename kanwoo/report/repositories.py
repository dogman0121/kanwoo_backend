from abc import abstractmethod, ABC
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from kanwoo.repositories import BaseRepository

from .models import MangaReport, ChapterReport, Report, CommentReport


class ReportRepository(BaseRepository):

    def create_report(self, report):
        report.add(commit=True)

        return report
    
    def update_report(self, report, data):
        report.update(data, commit=True)

    def get_waiting_moderation_count(self):
        return self.db_session.execute(
            select(func.count("*"))
            .where(Report.resolved_at == None)
        ).scalar()

    def get_all_reports(self, resolved = None):
        q = select(Report)

        if resolved is None:
            pass
        else:
            if resolved:
                q = q.filter(Report.resolved_at.isnot(None))
            else:
                q = q.filter(Report.resolved_at.is_(None))

        return self.db_session.execute(
            q.order_by(Report.created_at)
        ).scalars().all()

    def get_report_by_id(self, report_id):
        return self.db_session.execute(
            select(Report)
            .filter(Report.id == report_id)
        ).scalar()



class MangaReportRepository(ReportRepository):

    def create_manga_report(self, report):
        report.add(commit=True)

        return report
    
    def get_manga_waiting_moderation_count(self):
        return self.db_session.execute(
            select(func.count("Report.id"))
            .join(Report, MangaReport.report_id == Report.id)
            .filter(MangaReport.manga_id != None, Report.resolved_at == None)
        ).scalar()
    
    def get_all_manga_reports(self, resolved=None):
        q = select(Report).join(MangaReport, MangaReport.report_id == Report.id).filter(MangaReport.manga_id != None)

        if resolved is None:
            pass
        else:
            if resolved:
                q = q.filter(Report.resolved_at.isnot(None))
            else:
                q = q.filter(Report.resolved_at.is_(None))

        return self.db_session.execute(q.order_by(Report.created_at)).scalars().all()

class ChapterReportRepository(ReportRepository):

    def create_chapter_report(self, report):
        report.add(commit=True)

        return report

    def get_chapter_waiting_moderation_count(self):
        return self.db_session.execute(
            select(func.count("Report.id"))
            .join(ChapterReport, ChapterReport.report_id == Report.id)
            .where(Report.resolved_at == None)
        ).scalar()
        
    def get_all_chapter_reports(self, resolved=None):
        q = select(Report).join(ChapterReport, ChapterReport.report_id == Report.id).filter(ChapterReport.manga_id != None)

        if resolved is None:
            pass
        else:
            if resolved:
                q = q.filter(Report.resolved_at.isnot(None))
            else:
                q = q.filter(Report.resolved_at.is_(None))

        return self.db_session.execute(q.order_by(Report.created_at)).scalars().all()
    

class CommentReportRepository(ReportRepository):

    def create_chapter_report(self, report):
        report.add(commit=True)

        return report

    def get_chapter_waiting_moderation_count(self):
        return self.db_session.execute(
            select(func.count("Report.id"))
            .join(CommentReport, CommentReport.report_id == Report.id)
            .where(Report.resolved_at == None)
        ).scalar()
        
    def get_all_chapter_reports(self, resolved=None):
        q = select(Report).join(CommentReport, CommentReport.report_id == Report.id).filter(CommentReport.manga_id != None)

        if resolved is None:
            pass
        else:
            if resolved:
                q = q.filter(Report.resolved_at.isnot(None))
            else:
                q = q.filter(Report.resolved_at.is_(None))

        return self.db_session.execute(q.order_by(Report.created_at)).scalars().all()


