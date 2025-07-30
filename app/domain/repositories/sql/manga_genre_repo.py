from abc import ABC, abstractmethod

class MangaGenreRepository(ABC):
    @abstractmethod
    def get_by_id(self, genre_id):
        pass