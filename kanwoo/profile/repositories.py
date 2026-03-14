from sqlalchemy import select

from kanwoo.repositories import BaseRepository

from .models import Profile, ProfileAvatar, ProfileLink

from typing import List

class ProfileRepository(BaseRepository):

    def create_profile(self, profile: Profile):
        profile.add()

        return profile
    
    def delete_avatar(self, profile: Profile):
        if profile.avatar:
            profile.avatar.delete()
            
        return profile
    
    def update_avatar(self, profile: Profile, avatar: ProfileAvatar):
        old_avatar = profile.avatar

        profile.avatar = avatar

        if old_avatar:
            old_avatar.delete(commit=True)

        return profile

    
    def add_links(self, profile: Profile, links: List[ProfileLink]):
        old_links = profile.links

        profile.links = links

        for i in old_links:
            i.delete()

        return profile

    def save_profile(self, profile: Profile):
        profile.save()

    def system_get_profile_by_slug(self, slug: str) -> Profile:
        return self.db_session.execute(select(Profile).filter_by(slug=slug)).scalar()

    def user_get_profile_by_slug(self, slug: str) -> Profile:
        return self.db_session.execute(select(Profile).filter_by(slug=slug)).scalar()
    
    def system_get_profile_by_id(self, profile_id):
        return self.db_session.execute(select(Profile).filter_by(id=profile_id)).scalar()

    def user_get_profile_by_id(self, profile_id):
        return self.db_session.execute(select(Profile).filter_by(id=profile_id)).scalar()
    
    def get_user_profiles(self, user_id):
        owned = self.db_session.execute(select(Profile).filter_by(creator_id=user_id)).scalars().all()

        return owned
    
    def user_get_profile_by_slug_from_user(self, user_id, profile_slug):
        self.db_session.execute(select(Profile).filter_by(creator_id=user_id, slug=profile_slug)).scalar()