from dataclasses import dataclass
from io import BytesIO


@dataclass
class UploadFile:
    filename: str
    content_type: str
    bytes: BytesIO