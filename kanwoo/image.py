from kanwoo.entity import File

from typing import Tuple
from PIL import Image
import io

class ImageService:
    def __init__(self, image: File, output_format: str = None):
        self.file = image
        self._image = Image.open(io.BytesIO(image.bytes))
        
        self.output_format = output_format or self._image.format or 'JPEG'
        
        if self.output_format == "JPEG":
            self._image = self._image.convert("RGB")

    def resize(self, size: Tuple[int, int], fit=False) -> File:
        if fit:
            self._image = self._image.resize(size, Image.Resampling.LANCZOS)
        else:
            self._image.thumbnail(size, Image.Resampling.LANCZOS)

        output = io.BytesIO()
        self._image.save(output, format=self._image.format or 'JPEG')

        new_file = File(
            filename=self.file.filename,
            content_type=self.file.content_type,
            bytes=output.getvalue()
        )

        return new_file
    
class ImageServiceFactory:

    def __init__(self):
        pass

    def create(self, image: File, output_format: str = None):
        return ImageService(image, output_format)
