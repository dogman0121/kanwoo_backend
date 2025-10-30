from .models import Profile, ProfileAvatar, ProfileLink

from typing import List

class ProfileRepository:
    @staticmethod
    def create_profile(profile: Profile):
        profile.add()

        return profile
    
    @staticmethod
    def delete_avatar(profile: Profile, avatar: ProfileAvatar):
        profile.avatar.delete()

        return profile
    
    @staticmethod
    def update_avatar(profile: Profile, avatar: ProfileAvatar):
        old_avatar = profile.avatar

        profile.avatar = avatar

        if old_avatar:
            old_avatar.delete(commit=True)

        return profile


    @staticmethod
    def update_team(profile: Profile, data: dict):
        profile.update(data)

        return profile
    
    @staticmethod
    def add_links(profile: Profile, links: List[ProfileLink]):
        old_links = profile.links

        profile.links = links

        for i in old_links:
            i.delete()

        return profile

    @staticmethod
    def save_profile(profile: Profile):
        profile.save()

    @staticmethod
    def get_by_slug(slug: str) -> Profile:
        return Profile.query.filter_by(slug=slug).first()
    
    @staticmethod
    def get_by_id(profile_id):
        return Profile.query.filter_by(id=profile_id).first()
    
    @staticmethod
    def get_user_profiles(user_id):
        owned = Profile.query.filter_by(creator_id=user_id).all()

        return owned