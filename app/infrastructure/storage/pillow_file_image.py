import copy
from io import BytesIO
from typing import Tuple

from PIL import Image

from app.domain.entities.file import UploadFile
from app.domain.entities.file.image_file import ImageFile
from app.infrastructure.storage.file import File


class PillowFileImage(ImageFile, File):
    def __init__(self, file: UploadFile):
        self.file = file
        self.img = Image.open(file.bytes)

    @property
    def size(self):
        return self.img.size

    @property
    def content(self):
        return BytesIO(self.img.tobytes())

    def resize(self, size: Tuple[int, int]):
        self.img = self.img.resize(size)

    def convert(self, mode: str):
        self.img.convert(mode)

    def copy(self):
        return copy.deepcopy(self)