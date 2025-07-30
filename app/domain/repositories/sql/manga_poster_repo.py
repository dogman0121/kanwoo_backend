from abc import abstractmethod, ABC

from app.domain.entities.manga import Manga
from app.domain.entities.manga.manga_poster import MangaPoster


class MangaPosterRepository(ABC):
    @abstractmethod
    def create(self, manga: Manga, orig_filename: str, order: int) -> MangaPoster:
        pass

    def delete(self, poster: MangaPoster) -> None:
        pass
