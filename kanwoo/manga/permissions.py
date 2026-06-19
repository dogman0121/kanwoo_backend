from kanwoo.permissions import ADMIN_ROLE

from .models import Manga

class MangaPolicy:

    def can_view(self, profile, manga: Manga):
        return True

    def can_create(self, creator_profile, author_profile):
        if creator_profile.role >= ADMIN_ROLE:
            return True

        return creator_profile.id == author_profile.id

    def can_edit(self, profile, manga: Manga):
        if profile.role >= ADMIN_ROLE:
            return True
        
        if profile is None:
            return False
        
        return profile.id == manga.creator_id
    
    def can_delete(self, profile, manga: Manga):
        if profile is None:
            return False
        return profile.id == manga.creator_id
    
    def can_create_translation(self, profile, manga: Manga, official: bool = False):
        if profile is None:
            return False
        if official:
            return profile.id == manga.creator_id
        
        return True