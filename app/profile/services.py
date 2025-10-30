from pytils.translit import slugify

from .dto import ProfileCreateDTO, ProfileUpdateDTO
from .models import Profile, ProfileAvatar, ProfileLink
from .repositories import ProfileRepository
from .exceptions import ProfileNotFoundException, ProfileUpdateNotAllowedException
from .permissions import ProfilePolicy
from .schemas import AvatarAction

from app import storage
from app.uuid import UUID
from app.user.models import User


class ProfileService:
    def __init__(self, user: User):
        self.user = user

    def create_profile(self, data: ProfileCreateDTO): 
        slug = slugify(data.name)

        # check if slug has been taken
        try:
            i = 1
            while self.get_profile_by_slug(slug):
                slug = slugify(data.name) + str(i)
                i+=1
        except ProfileNotFoundException:
            pass

        profile = Profile(
            name=data.name,
            slug=slug,
            about=data.about,
            creator_id=self.user.id,
        )

        ProfileRepository.create_profile(profile)

        ProfileRepository.save_team(profile)

        return profile
    

    def update_profile(self, profile: Profile, data: ProfileUpdateDTO):
        if not ProfilePolicy(self.user).can_edit(profile):
            raise ProfileUpdateNotAllowedException


        new_avatar, old_avatar = None, None
        if data.avatar_action == AvatarAction.REMOVE and profile.avatar:
            old_avatar = profile.avatar

        elif data.avatar_action == AvatarAction.UPDATE:
            new_avatar_uuid = UUID.generate_uuid()
            storage.save(data.avatar, f'profiles/{profile.id}/{new_avatar_uuid}.jpg')
            
            new_avatar = ProfileAvatar(
                uuid=new_avatar_uuid,
                orig_filename=data.avatar.filename,
                ext=".jpg"
            )

            old_avatar = profile.avatar
        else:
            new_avatar = profile.avatar

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
            "avatar": new_avatar
        }, commit=True)

        if old_avatar:
            storage.delete(f"profile/{profile.id}/{old_avatar.uuid}{old_avatar.ext}")

        return profile
        
    def get_profiles(self):
        return ProfileRepository.get_user_profiles(self.user.id)

    @staticmethod
    def get_profile_by_slug(slug: str) -> Profile:
        profile = ProfileRepository.get_by_slug(slug)

        if profile is None:
            raise ProfileNotFoundException

        return profile
    
    @staticmethod
    def get_profile_by_id(profile_id):
        profile = ProfileRepository.get_by_id(profile_id)

        if profile is None:
            raise ProfileNotFoundException
        return profile