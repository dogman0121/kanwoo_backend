from typing import Optional, List
from dataclasses import dataclass

from kanwoo.chapter.models import Chapter
from kanwoo.manga.models import Manga
from kanwoo.translation.models import Translation

@dataclass
class CreateReadingProgressDTO:
    chapter: Chapter
    page: Optional[int]

@dataclass
class UpdateReadingProgressDTO:
    page: int

@dataclass
class ReadingProgressContextDTO:
    chapter: Optional[Chapter]
    manga: Optional[Manga]
    translation: Optional[Translation]
