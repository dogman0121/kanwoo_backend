from abc import ABC, abstractmethod
from io import BytesIO


class File(ABC):
    content: BytesIO