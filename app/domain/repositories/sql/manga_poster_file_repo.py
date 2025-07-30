from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.manga.manga_poster import MangaPoster
from app.domain.entities.manga.manga_poster_file import MangaPosterFile


class MangaPosterFileRepository(ABC):
    @abstractmethod
    def create(self, poster: MangaPoster, file_type, file_uuid):
        pass

    @abstractmethod
    def get_versions(self, poster_uuid: str) -> List[MangaPosterFile]:
        pass
