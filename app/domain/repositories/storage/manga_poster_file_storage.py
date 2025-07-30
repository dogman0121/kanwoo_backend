from abc import ABC, abstractmethod
from typing import Tuple

from app.domain.entities.manga import Manga
from app.domain.entities.file.upload_file import UploadFile


class MangaPosterFileStorage(ABC):
    @abstractmethod
    def save(self, manga_id: int, poster_file: UploadFile, file_size: Tuple[int, int]) -> str:
        pass

    @abstractmethod
    def delete(self, manga_id: int, file_uuid: str, file_ext:str) -> None:
        pass

    @abstractmethod
    def get_link(self, manga_id: int, file_uuid: str) -> str:
        pass