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
from kanwoo.collection.containers import CollectionContainer
from kanwoo.database import DBTransaction
from kanwoo.settings.containers import SettingsContainer
from kanwoo.comment.containers import CommentContainer
from kanwoo.post.containers import PostContainer
from kanwoo.notification.containers import NotificationContainer

class AppContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    db_session = providers.Dependency()

    file_storage = providers.Dependency()

    cache = providers.Dependency()

    db_transaction = providers.Factory(
        DBTransaction,
        db_session=db_session
    )

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
        user_service=user_container.user_service,
        config=config,
        db_transaction=db_transaction,
        user_repo=user_container.user_repo,
        db_session=db_session
    )

    main_container = providers.Container(
        MainContainer,
        db_session=db_session
    )

    reading_progress_container = providers.Container(
        ReadingProgressContainer,
        db_session=db_session,
        db_transaction=db_transaction
    )

    profile_container = providers.Container(
        ProfileContainer,
        db_session=db_session,
        file_storage=file_storage,
        image_service_factory=image_service_factory,
        db_transaction=db_transaction
    )

    manga_container = providers.Container(
        MangaContainer,
        image_service_factory=image_service_factory,
        file_storage=file_storage,
        db_session=db_session,
        moderation_service=moderation_container.moderation_service,
        db_transaction=db_transaction
    )

    translation_container = providers.Container(
        TranslationContainer,
        db_session=db_session,
        db_transaction=db_transaction
    )

    chapter_container = providers.Container(
        ChapterContainer,
        image_service_factory=image_service_factory,
        file_storage=file_storage,
        db_session=db_session,
        db_transaction=db_transaction
    )

    home_container = providers.Container(
        HomeContainer,
        db_session=db_session,
        reading_progress_service=reading_progress_container.reading_progress_service
    )

    report_container = providers.Container(
        ReportContainer,
        db_transaction=db_transaction,
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

    collection_container = providers.Container(
        CollectionContainer,
        db_session=db_session,
        db_transaction= db_transaction,
        manga_repo = manga_container.manga_repo
    )

    settings_container = providers.Container(
        SettingsContainer
    )

    post_container = providers.Container(
        PostContainer,
        db_session=db_session,
        db_transaction=db_transaction
    )
    notification_container = providers.Container(
        NotificationContainer,
        db_session=db_session,
        db_transaction=db_transaction
    )

    comment_container = providers.Container(
        CommentContainer,
        db_session=db_session,
        db_transaction=db_transaction
    )