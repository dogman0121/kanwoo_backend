from .models import Profile

from kanwoo.user.models import User

class ProfileAuthPolicy:
    
    def can_use(self, user: User, profile: Profile):
        if user and user.id == profile.owner_id:
            return True
        return False


class ProfilePolicy:

    def can_view_manga(self, current_profile: Profile, profile: Profile):
        return True
    
    def can_edit(self, current_profile, profile: Profile):
        if current_profile and current_profile.id == profile.id:
            return True
        
        return False