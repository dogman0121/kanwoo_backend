from dataclasses import dataclass
from werkzeug.datastructures import FileStorage
import enum

def to_file(file: FileStorage):
    if not isinstance(file, FileStorage):
        raise ValueError("File is not instance of FileStorage.")
    
    return File(
        filename=file.filename,
        content_type=file.content_type,
        bytes=file.stream.read()
    )

class FileAction(enum.Enum):
    KEEP = "keep"
    UPDATE = "update"
    DELETE = "delete"

@dataclass
class File:
    filename: str
    content_type: str
    bytes: bytes

    def __repr__(self):
        return f"<File: {self.filename}>"