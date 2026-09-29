from kanwoo.entity import File

from typing import Tuple
from PIL import Image, ImageOps
import io

class Img:
    width: str
    height: str
    file: File

    def __init__(self, filename, content_type, bytes, width, height):
        self.width = width
        self.height = height
        self.file = File(filename, content_type, bytes)

    @property
    def filename(self):
        return self.file.filename

    @property
    def content_type(self):
        return self.file.content_type

    @property
    def bytes(self):
        return self.file.bytes

    def __repr__(self):
        return f"<Image: {self.filename}>"
        

class ImageService:
    def __init__(self, image: File, output_format: str = None):
        self.file = image
        self._image = Image.open(io.BytesIO(image.bytes))
        
        self.output_format = output_format or self._image.format or 'JPEG'
        
        if self.output_format == "JPEG":
            self._image = self._image.convert("RGB")

    def resize(self, size: Tuple[int, int], fit=False) -> Image:
        original_format = self._image.format or 'JPEG'
        
        img_copy = self._image.copy()

        if fit:
            img_copy = ImageOps.fit(img_copy, size, method=Image.Resampling.LANCZOS)
        else:
            img_copy.thumbnail(size, Image.Resampling.LANCZOS)

        output = io.BytesIO()
        
        if original_format.upper() in ['JPEG', 'JPG'] and img_copy.mode == 'RGBA':
            img_copy = img_copy.convert('RGB')

        img_copy.save(output, format=original_format)

        return Img(
            filename=self.file.filename,
            content_type=self.file.content_type,
            bytes=output.getvalue(),
            width=self._image.width,
            height=self._image.height
        )
    
class ImageServiceFactory:

    def __init__(self):
        pass

    def create(self, image: File, output_format: str = None):
        return ImageService(image, output_format)
