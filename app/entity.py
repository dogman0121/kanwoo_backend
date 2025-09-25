from dataclasses import dataclass
from werkzeug.datastructures import FileStorage

def to_file(file: FileStorage):
    if not isinstance(file, FileStorage):
        raise ValueError("File is not instance of FileStorage.")
    
    return File(
        filename=file.name,
        content_type=file.content_type,
        content=file.stream.read()
    )

@dataclass
class File:
    filename: str
    content_type: str
    bytes: bytes