from datetime import datetime

from kanwoo.database import DBTransaction

from .models import ChapterReport, MangaReport, Report, CommentReport
from .dto import ReportCreateDTO
from .repositories import MangaReportRepository, ChapterReportRepository, ReportRepository, CommentReportRepository


class ReportService:
    
    def __init__(
        self, 
        report_repo: ReportRepository,
        chapter_report_repo: ChapterReportRepository, 
        manga_report_repo: MangaReportRepository,
        comment_report_repo: CommentReportRepository,
        db_transaction: DBTransaction
    ):
        self.report_repo = report_repo
        self.chapter_report_repo = chapter_report_repo
        self.manga_report_repo = manga_report_repo
        self.comment_report_repo = comment_report_repo
        self.db_transaction = db_transaction
    

    def user_create_manga_report(self, profile, manga, report_data: ReportCreateDTO):
        with self.db_transaction:
            report = Report(
                type_id=report_data.type_id,
                comment=report_data.comment,
                creator_id=profile.id if profile else None,
            )

            self.report_repo.create_report(report)

            manga_report = MangaReport(
                report_id = report.id,
                manga_id=manga.id
            )

            self.manga_report_repo.create_manga_report(manga_report)

    def user_create_chapter_report(self, profile, chapter, report_data: ReportCreateDTO):
        with self.db_transaction:
            report = Report(
                type_id=report_data.type_id,
                comment=report_data.comment,
                creator_id=profile.id if profile else None,
            )

            self.report_repo.create_report(report)

            chapter_report = ChapterReport(
                report_id = report.id,
                chapter_id=chapter.id
            )

            self.chapter_report_repo.create_chapter_report(chapter_report)

    def user_create_comment_report(self, profile, comment, report_data: ReportCreateDTO):
        with self.db_transaction:
            report = Report(
                type_id=report_data.type_id,
                comment=report_data.comment,
                creator_id=profile.id if profile else None,
            )

            self.report_repo.create_report(report)

            comment_report = ChapterReport(
                report_id = report.id,
                comment_id=comment.id
            )

            self.comment_report_repo.create_comment_report(comment_report)

    def user_get_all_chapters_reports(self, profile, resolved=None):
        return self.chapter_report_repo.get_all_reports(resolved=resolved)

    def user_get_all_manga_reports(self, profile, resolved=None):
        return self.manga_report_repo.get_all_reports(resolved=resolved)

    def user_get_chapter_report_by_id(self, profile, report_id):
        return self.chapter_report_repo.get_report_by_id(report_id)

    def user_get_manga_report_by_id(self, profile, report_id):
        return self.manga_report_repo.get_report_by_id(report_id)

    def user_resolve_report(self, profile, report):
        self.report_repo.update_report(
            report, 
            {
                "resolver_id": profile.id,
                "resolved_at": datetime.now()
            })
        
        return report      

    def user_get_manga_active_reports_count(self, profile):
        return self.manga_report_repo.get_manga_waiting_moderation_count()

    def user_get_chapter_active_reports_count(self, profile):
        return self.chapter_report_repo.get_chapter_waiting_moderation_count()