from kanwoo.entity import File

from typing import Tuple
from PIL import Image, ImageOps
import io

class ImageService:
    def __init__(self, image: File, output_format: str = None):
        self.file = image
        self._image = Image.open(io.BytesIO(image.bytes))
        
        self.output_format = output_format or self._image.format or 'JPEG'
        
        if self.output_format == "JPEG":
            self._image = self._image.convert("RGB")

    def resize(self, size: Tuple[int, int], fit=False) -> File:
        original_format = self._image.format or 'JPEG'
        
        img_copy = self._image.copy()

        if fit:
            img_copy = ImageOps.fit(img_copy, size, Image.Resampling.LANCZOS)
        else:
            img_copy.thumbnail(size, Image.Resampling.LANCZOS)

        output = io.BytesIO()
        
        if original_format.upper() in ['JPEG', 'JPG'] and img_copy.mode == 'RGBA':
            img_copy = img_copy.convert('RGB')

        img_copy.save(output, format=original_format)

        return File(
            filename=self.file.filename,
            content_type=self.file.content_type,
            bytes=output.getvalue()
        )
    
class ImageServiceFactory:

    def __init__(self):
        pass

    def create(self, image: File, output_format: str = None):
        return ImageService(image, output_format)
