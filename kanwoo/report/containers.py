from dependency_injector import containers, providers

from .repositories import ChapterReportRepository, MangaReportRepository
from .services import ReportService

class ReportContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    chapter_report_repo = providers.Singleton(
        ChapterReportRepository,
        db_session=db_session
    )

    manga_report_repo = providers.Singleton(
        MangaReportRepository,
        db_session=db_session
    )

    report_service = providers.Factory(
        ReportService,
        chapter_report_repo=chapter_report_repo,
        manga_report_repo=manga_report_repo
    )

