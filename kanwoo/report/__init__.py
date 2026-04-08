from dependency_injector import containers, providers

from .repositories import ReportRepository
from .services import ReportService

class ReportContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    report_repo = providers.Singleton(
        ReportRepository,
        db_session=db_session
    )

    report_service = providers.Factory(
        ReportService,
        report_repo=report_repo
    )

