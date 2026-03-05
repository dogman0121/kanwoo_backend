from .models import Profile

from kanwoo.user.models import User

class ProfileAuthPolicy:
    
    def can_use(self, user: User, profile: Profile):
        if user and user.id == profile.creator_id:
            return True
        return False


class ProfilePolicy:

    def can_view_manga(self, user_profile: Profile, profile: Profile):
        return True
    
    def can_edit(self, curr_profile: User, profile: Profile):
        if curr_profile and curr_profile.id == profile.creator_id:
            return True
        
        return False