from abc import ABC, abstractmethod
from typing import Tuple

class ImageFile(ABC):

    @abstractmethod
    def resize(self, size: Tuple[int, int]):
        pass

    @abstractmethod
    def convert(self, mode: str) -> None:
        pass

    @abstractmethod
    def copy(self):
        pass