from pytils.translit import slugify

from kanwoo.image import ImageServiceFactory
from kanwoo.file_storage import FileStorage
from kanwoo.uuid import UUID

from .dto import ProfileCreateDTO, ProfileUpdateDTO
from .models import Profile, ProfileAvatar, ProfileLink
from .repositories import ProfileRepository
from .exceptions import ProfileNotFoundException, ProfileUpdateNotAllowedException, ProfileAlreadyExistsException
from .schemas import AvatarAction
from .permissions import ProfileAuthPolicy, ProfilePolicy

class ProfileAvatarService:
    AVATAR_SIZE = (120, 120)

    def __init__(
            self, 
            storage: FileStorage,
            image_service_factory: ImageServiceFactory, 
            profile_repo: ProfileRepository
        ):
        self.image_service_factory = image_service_factory
        self.profile_repo = profile_repo
        self.storage = storage

    def __get_avatar_path(self, uuid, ext):
        return f"profiles/{uuid}{ext}"

    def update_profile_avatar(self, profile, avatar_file):
        image_service = self.image_service_factory.create(avatar_file, "JPEG")
        
        avatar_resized_file = image_service.resize(self.AVATAR_SIZE)
        avatar_uuid = UUID.generate_uuid()

        avatar_path = self.__get_avatar_path(avatar_uuid, ".jpg")

        profile_avatar = ProfileAvatar(
            uuid=avatar_uuid,
            orig_filename=avatar_file.filename,
            path=avatar_path
        )

        self.storage.save(avatar_resized_file, avatar_path)

        profile.avatar = profile_avatar


    def delete_profile_avatar(self, profile):
        self.profile_repo.delete_avatar(profile)


class ProfileAuthService:

    def __init__(
            self, 
            profile_avatar_service: ProfileAvatarService,
            profile_repo: ProfileRepository, 
            profile_auth_policy: ProfileAuthPolicy,
        ):
        self.profile_avatar_service = profile_avatar_service
        self.profile_repo = profile_repo
        self.profile_auth_policy = profile_auth_policy

    def _create_profile(self, data: ProfileCreateDTO):
        slug = ""

        if data.slug:
            try:
                self.system_get_profile_by_slug(slug)

                raise ProfileAlreadyExistsException
            except ProfileNotFoundException:
                slug = data.slug
        else:
            tmp_slug = slugify(data.name)

            # check if slug has been taken
            try:
                i = 1
                while self.system_get_profile_by_slug(tmp_slug):
                    slug = slugify(data.name) + str(i)
                    i+=1
            except ProfileNotFoundException:
                slug = tmp_slug

        profile = Profile(
            name=data.name,
            slug=slug,
            about=data.about,
            creator_id=data.creator_id,
        )

        self.profile_repo.create_profile(profile)

        return profile
    
    def user_create_profile(self, user, data: ProfileCreateDTO): 
        if user.id != data.creator_id:
            raise ValueError("User must be creator")
        return self._create_profile(data)
    
    def system_create_profile(self, data: ProfileCreateDTO):
        return self._create_profile(data)
    
    def system_get_profile_by_id(self, profile_id):
        profile = self.profile_repo.system_get_profile_by_id(profile_id)

        if profile is None:
            raise ProfileNotFoundException
        return profile
    
    def system_get_profile_by_slug(self, slug: str) -> Profile:
        profile = self.profile_repo.system_get_profile_by_slug(slug)

        if profile is None:
            raise ProfileNotFoundException

        return profile
        
    def user_get_user_profiles(self, user):
        return self.profile_repo.get_user_profiles(user.id)
    
    def system_check_user_access_for_profile(self, user, profile):
        return self.profile_auth_policy.can_use(user, profile)
        

class ProfileService:

    def __init__(
            self, 
            profile_repo: ProfileRepository,
            profile_policy: ProfilePolicy
        ):
        self.profile_repo = profile_repo
        self.profile_policy = profile_policy

    def user_get_profile_by_slug(self, profile, slug: str) -> Profile:
        profile = self.profile_repo.user_get_profile_by_slug(slug)

        if profile is None:
            raise ProfileNotFoundException

        return profile
    
    def system_get_profile_by_slug(self, slug):
        profile = self.profile_repo.system_get_profile_by_slug(slug)

        if profile is None:
            raise ProfileNotFoundException

        return profile

    def user_get_profile_by_id(self, profile, profile_id):
        profile = self.profile_repo.user_get_profile_by_id(profile_id)

        if profile is None:
            raise ProfileNotFoundException
        return profile

    def user_update_profile(self, curr_profile, profile: Profile, data: ProfileUpdateDTO):
        if not self.profile_policy.can_edit(curr_profile, profile):
            raise ProfileUpdateNotAllowedException
        
        if data.avatar_action == AvatarAction.REMOVE:
            self.profile_avatar_service.delete_profile_avatar(profile)
        elif data.avatar_action == AvatarAction.UPDATE:
            self.profile_avatar_service.update_profile_avatar(profile, data.avatar)

        if data.links:
            links = [
                ProfileLink(
                    name=l.name,
                    link=l.link
                ) for l in data.links
            ]
        else:
            links = []

        profile.update({
            "name": data.name,
            "slug": data.slug,
            "about": data.about,
            "links": links,
        }, commit=True)

        return profile