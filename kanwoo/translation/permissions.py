from typing import Optional

from kanwoo.permissions import ADMIN_ROLE
from kanwoo.profile.models import Profile

from .models import Translation

class TranslationPolicy:

    def can_create(self, creator_profile, owner_profile):
        if creator_profile.role >= ADMIN_ROLE:
            return True
        
        return creator_profile.id == owner_profile.id 

    def can_edit(self, profile, translation: Translation):
        if profile is None: return False
        return profile.id == translation.creator_id
    
    def can_view(self, profile, translation: Translation, by_link = False):
        if by_link and translation.privacy_id == 3: return True
        if translation.privacy_id == 1: return True # public
        if profile and translation.creator_id == profile.id: return True
        return False
    
    def can_delete(self, profile, translation: Translation):
        return translation.creator_id == profile.id