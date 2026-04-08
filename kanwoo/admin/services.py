from __future__ import annotations
from typing import TYPE_CHECKING

from kanwoo.report.services import ReportService
from kanwoo.manga.services import MangaSuggestionService, MangaService
from kanwoo.main.services import FeedbackService

from .dto import AdminMainDashboardDTO
from .repositories import AdminMangaRepository

if TYPE_CHECKING:
    from kanwoo.report.services import ReportService
    from kanwoo.manga.services import MangaSuggestionService
    from kanwoo.moderation.services import ModerationService
    from kanwoo.main.services import FeedbackService

class AdminDashboardService:

    def __init__(
            self, 
            report_service: ReportService, 
            manga_suggestion_service: MangaSuggestionService, 
            moderation_service: ModerationService, 
            feedback_service: FeedbackService
        ):
        self.report_service = report_service
        self.manga_suggestion_service = manga_suggestion_service
        self.moderation_service = moderation_service
        self.feedback_service = feedback_service
        

    def user_get_main_dashboard(self, profile):
        manga_reports_count = self.report_service.user_get_manga_active_reports_count(profile)
        chapters_reports_count = self.report_service.user_get_chapter_active_reports_count(profile)
        manga_suggestion_count = self.manga_suggestion_service.user_get_unresolved_suggestions_count(profile)
        chapter_waiting_moderation_count = self.moderation_service.user_get_chapter_waiting_moderation_count(profile)
        manga_waiting_moderation_count = self.moderation_service.user_get_manga_waiting_moderation_count(profile)
        feedback_unread_messages_count = self.feedback_service.user_get_unread_feedback_count(profile)

        return AdminMainDashboardDTO(
            manga_reports_count=manga_reports_count,
            chapters_reports_count=chapters_reports_count,
            manga_sugesstions_count=manga_suggestion_count,
            manga_waiting_moderation_count=manga_waiting_moderation_count,
            chapter_waiting_moderation_count=chapter_waiting_moderation_count,
            feedback_messages_count=feedback_unread_messages_count
        )


class AdminMangaService:

    def __init__(
            self, 
            admin_manga_repo: AdminMangaRepository,
        ):
        self.admin_manga_repo = admin_manga_repo

    def user_get_manga_list(self, profile, filter):
        return self.admin_manga_repo.get_manga_list(filter.query, filter.statuses)

    def user_get_manga_by_slug(self, profile, manga_slug: str):
        return self.admin_manga_repo.get_manga(manga_slug)
