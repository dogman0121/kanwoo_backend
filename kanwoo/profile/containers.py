from dependency_injector import containers, providers

from .repositories import ProfileRepository
from .services import ProfileAuthService, ProfileAvatarService, ProfileService
from .permissions import ProfilePolicy, ProfileAuthPolicy

class ProfileContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    image_service_factory = providers.Dependency()

    file_storage = providers.Dependency()

    profile_repo = providers.Singleton(
        ProfileRepository,
        db_session
    )

    profile_avatar_service = providers.Factory(
        ProfileAvatarService,
        image_service_factory=image_service_factory,
        storage=file_storage,
        profile_repo=profile_repo
    )

    profile_auth_policy = providers.Singleton(
        ProfileAuthPolicy
    )

    profile_policy = providers.Singleton(
        ProfilePolicy
    )

    profile_auth_service = providers.Factory(
        ProfileAuthService,
        profile_repo=profile_repo,
        profile_auth_policy=profile_auth_policy
    )

    profile_service = providers.Factory(
        ProfileService,
        profile_repo=profile_repo,
        profile_avatar_service=profile_avatar_service,
        profile_policy=profile_policy
    )