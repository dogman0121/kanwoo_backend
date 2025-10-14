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
            while self.get_team_by_slug(slug):
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

        if data.avatar_action == AvatarAction.REMOVE and profile.avatar:
            storage.delete(f'profiles/{profile.id}/{profile.avatar.uuid}{profile.avatar.ext}')
            profile = ProfileRepository.delete_avatar(profile, profile.avatar)

        elif data.avatar_action == AvatarAction.UPDATE:
            old_avatar = profile.avatar
            
            new_avatar_uuid = UUID.generate_uuid()
            storage.save(data.avatar, f'profiles/{profile.id}/{new_avatar_uuid}.jpg')
            
            new_avatar = ProfileAvatar(
                uuid=new_avatar_uuid,
                orig_filename=data.avatar.filename,
                ext=".jpg"
            )

            profile = ProfileRepository.update_avatar(profile, new_avatar)

            if old_avatar:
                storage.delete(f'profiles/{profile.id}/{old_avatar.uuid}.jpg')

        if data.links:
            links = [
                ProfileLink(
                    name=l.name,
                    link=l.link
                ) for l in data.links
            ]
        else:
            links = []

        profile = ProfileRepository.update_team(profile, {
            "name": data.name,
            "slug": data.slug,
            "about": data.about,
        })

        ProfileRepository.add_links(profile, links)

        ProfileRepository.save_profile(profile)

        return profile
        
    def get_profiles(self):
        return ProfileRepository.get_user_profiles(self.user.id)

    @staticmethod
    def get_team_by_slug(slug: str) -> Profile:
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