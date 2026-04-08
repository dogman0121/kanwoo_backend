from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from .models import Chapter

if TYPE_CHECKING:
    from kanwoo.profile.models import Profile

class ChapterPolicy:

    def can_edit(self, profile: Optional[Profile], chapter: Chapter):
        if profile is None: return False
        return chapter.creator_id == profile.id
    
    def can_view(self, profile: Optional[Profile], chapter: Chapter, by_link = False):
        if by_link and chapter.privacy_id == 3: return True
        if chapter.privacy_id == 1: return True # public
        if profile and chapter.creator_id == profile.id: return True
        return False
    
    def can_delete(self, profile: Optional[Profile], chapter: Chapter):
        if profile is None: return False
        return profile.id == chapter.creator_id