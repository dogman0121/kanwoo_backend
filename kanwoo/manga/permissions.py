from .models import Manga

class MangaPolicy:
    def __init__(self, profile):
        self.profile = profile

    def can_edit(self, manga:Manga):
        return self.profile.id == manga.creator_id