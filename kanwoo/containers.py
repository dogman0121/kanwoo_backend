from dependency_injector import containers, providers

from kanwoo.email import EmailService
from kanwoo.image import ImageServiceFactory
from kanwoo.user.containers import UserContainer
from kanwoo.main.containers import MainContainer
from kanwoo.auth.containers import AuthContainer
from kanwoo.profile.containers import ProfileContainer
from kanwoo.manga.containers import MangaContainer
from kanwoo.translation.containers import TranslationContainer
from kanwoo.chapter.containers import ChapterContainer
from kanwoo.home.containers import HomeContainer
from kanwoo.moderation.containers import ModertionContainer
from kanwoo.report.containers import ReportContainer
from kanwoo.admin.containers import AdminContainer
from kanwoo.reading_progress.containers import ReadingProgressContainer
from kanwoo.search.containers import SearchContainer


class AppContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        [
            "kanwoo.middleware",
            "kanwoo.routes",
            "kanwoo.home.routes",
            "kanwoo.main.routes",
            "kanwoo.auth.routes",
            "kanwoo.chapter.routes",
            "kanwoo.translation.routes",
            "kanwoo.manga.routes",
            "kanwoo.profile.routes",
            "kanwoo.admin.routes",
            "kanwoo.search.routes"
        ]
    )

    config = providers.Configuration()

    db_session = providers.Dependency()

    file_storage = providers.Dependency()

    cache = providers.Dependency()

    email_service = providers.Factory(
        EmailService
    )

    moderation_container = providers.Container(
        ModertionContainer,
        db_session=db_session
    )

    image_service_factory = providers.Factory(
        ImageServiceFactory
    )

    user_container = providers.Container(
        UserContainer,
        db_session=db_session
    )

    auth_container = providers.Container(
        AuthContainer,
        email_service=email_service,
        cache=cache,
        user_service=user_container.user_service
    )

    main_container = providers.Container(
        MainContainer,
        db_session=db_session
    )

    reading_progress_container = providers.Container(
        ReadingProgressContainer,
        db_session=db_session
    )

    profile_container = providers.Container(
        ProfileContainer,
        db_session=db_session,
        file_storage=file_storage,
        image_service_factory=image_service_factory
    )

    manga_container = providers.Container(
        MangaContainer,
        image_service_factory=image_service_factory,
        file_storage=file_storage,
        db_session=db_session,
        moderation_service=moderation_container.moderation_service
    )

    translation_container = providers.Container(
        TranslationContainer,
        db_session=db_session
    )

    chapter_container = providers.Container(
        ChapterContainer,
        image_service_factory=image_service_factory,
        file_storage=file_storage,
        db_session=db_session
    )

    home_container = providers.Container(
        HomeContainer,
        db_session=db_session
    )

    report_container = providers.Container(
        ReportContainer,
        db_session=db_session
    )

    admin_container = providers.Container(
        AdminContainer,
        db_session=db_session,
        main_container=main_container,
        moderation_container=moderation_container,
        manga_container=manga_container,
        report_container=report_container
    )

    search_container = providers.Container(
        SearchContainer,
        db_session=db_session
    )