from .models import ChapterReport, MangaReport
from .dto import ReportCreateDTO
from .repositories import MangaReportRepository, ChapterReportRepository
from datetime import datetime

class ReportService:
    
    def __init__(
        self, 
        chapter_report_repo: ChapterReportRepository, 
        manga_report_repo: MangaReportRepository
    ):
        self.chapter_report_repo = chapter_report_repo
        self.manga_report_repo = manga_report_repo
        
    def user_create_manga_report(self, profile, manga, report_data: ReportCreateDTO):
        manga_report = MangaReport(
            type_id=report_data.type_id,
            comment=report_data.comment,
            creator_id=profile.id if profile else None,
            manga_id=manga.id
        )

        self.manga_report_repo.create_report(manga_report)

    def user_create_chapter_report(self, profile, chapter, report_data: ReportCreateDTO):
        chapter_report = ChapterReport(
            type_id=report_data.type_id,
            comment=report_data.comment,
            creator_id=profile.id if profile else None,
            chapter_id=chapter.id
        )

        self.chapter_report_repo.create_report(chapter_report)

    def user_get_all_chapters_reports(self, profile, resolved=None):
        return self.chapter_report_repo.get_all_reports(resolved=resolved)

    def user_get_all_manga_reports(self, profile, resolved=None):
        return self.manga_report_repo.get_all_reports(resolved=resolved)

    def user_get_chapter_report_by_id(self, profile, report_id):
        return self.chapter_report_repo.get_report_by_id(report_id)

    def user_get_manga_report_by_id(self, profile, report_id):
        return self.manga_report_repo.get_report_by_id(report_id)

    def user_resolve_chapter_report(self, profile, report):
        self.chapter_report_repo.update_report(
            report, 
            {
                "resolver_id": profile.id,
                "resolved_at": datetime.now()
            })
        
        return report

    def user_resolve_manga_report(self, profile, report):
        self.manga_report_repo.update_report(
            report, 
            {
                "resolver_id": profile.id,
                "resolved_at": datetime.now()
            })
        
        return report        

    def user_get_manga_active_reports_count(self, profile):
        return self.manga_report_repo.get_waiting_moderation_count()

    def user_get_chapter_active_reports_count(self, profile):
        return self.chapter_report_repo.get_waiting_moderation_count()