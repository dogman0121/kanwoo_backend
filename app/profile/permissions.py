from .models import Profile
from app.user.models import User

class ProfilePolicy:
    def __init__(self, user: User):
        self.user = user

    def can_edit(self, profile: Profile):
        if self.user.id == profile.creator_id:
            return True
        
        return False
    
    def can_use(self, profile: Profile):
        if self.user.id == profile.creator_id:
            return True
        return False