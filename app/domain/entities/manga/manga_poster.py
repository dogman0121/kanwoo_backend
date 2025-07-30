from dataclasses import dataclass
from typing import Optional

from app.domain.entities.manga.manga_poster_file import MangaPosterFile


@dataclass
class MangaPoster:
    uuid: str
    thumbnail: Optional[MangaPosterFile]
    small: Optional[MangaPosterFile]
    medium: Optional[MangaPosterFile]
    large: Optional[MangaPosterFile]
    order: int