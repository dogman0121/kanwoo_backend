class MangaPermission:
    def __init__(self, manga, user):
        self.manga = manga
        self.user = user

    def can_view(self):
        return self.manga.creator.id == self.user.id