from dataclasses import dataclass
from werkzeug.datastructures import FileStorage
from enum import Enum

def convert_to_file(file: FileStorage):
    if not isinstance(file, FileStorage):
        raise ValueError("File is not instance of FileStorage.")
    
    return File(
        filename=file.filename,
        content_type=file.content_type,
        bytes=file.stream.read()
    )

class FileAction(Enum):
    KEEP = "keep"
    UPDATE = "update"
    DELETE = "delete"

class Privacy(Enum):
    PRIVATE = 1,
    PUBLIC = 2,
    BY_LINK = 3

class FileType(Enum):
    POSTER_AVATAR = "poster_avatar"

@dataclass
class File:
    filename: str
    content_type: str
    bytes: bytes

    def __repr__(self):
        return f"<File: {self.filename}>"