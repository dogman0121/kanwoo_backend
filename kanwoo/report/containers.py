from dependency_injector import containers, providers

from .repositories import ChapterReportRepository, MangaReportRepository, ReportRepository, CommentReportRepository
from .services import ReportService

class ReportContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    db_transaction = providers.Dependency()

    report_repo = providers.Singleton(
        ReportRepository,
        db_session=db_session
    )

    chapter_report_repo = providers.Singleton(
        ChapterReportRepository,
        db_session=db_session
    )

    manga_report_repo = providers.Singleton(
        MangaReportRepository,
        db_session=db_session
    )

    comment_report_repo = providers.Singleton(
        CommentReportRepository,
        db_session=db_session
    )

    report_service = providers.Factory(
        ReportService,
        report_repo=report_repo,
        comment_report_repo=comment_report_repo,
        chapter_report_repo=chapter_report_repo,
        manga_report_repo=manga_report_repo,
        db_transaction=db_transaction
    )

