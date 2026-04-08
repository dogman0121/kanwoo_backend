from dependency_injector import containers, providers

from .repositories import AdminMangaRepository
from .services import AdminMangaService, AdminDashboardService

class AdminContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    moderation_container = providers.DependenciesContainer()
    manga_container = providers.DependenciesContainer()
    main_container = providers.DependenciesContainer()
    report_container = providers.DependenciesContainer()

    admin_manga_repo = providers.Singleton(
        AdminMangaRepository,
        db_session=db_session
    )

    admin_manga_service = providers.Factory(
        AdminMangaService,
        admin_manga_repo=admin_manga_repo,
    )

    admin_dashboard_service = providers.Factory(
        AdminDashboardService,
        report_service=report_container.report_service, 
        manga_suggestion_service=manga_container.manga_suggestion_service, 
        moderation_service=moderation_container.moderation_service,
        feedback_service=main_container.feedback_service,
    )
