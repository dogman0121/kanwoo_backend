from ..manga.repositories import MangaRepository

class HomeService:
    def __init__(self, profile):
        self.profile = profile

    def get_newest_manga(self):
        manga = MangaRepository.get_newest()
        return manga

    def get_ended_manga(self):
        manga = MangaRepository.get_newest()
        return manga

    def get_featured_manga(self):
        manga = MangaRepository.get_newest()
        return manga

    def get_profile_history(self):
        pass

    def get_random_manga(self):
        manga = MangaRepository.get_newest()
        return manga