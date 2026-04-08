from typing import Optional

from kanwoo.profile.models import Profile

from .models import Translation

class TranslationPolicy:

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