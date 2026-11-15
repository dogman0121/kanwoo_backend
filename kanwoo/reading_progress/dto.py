from typing import Optional, List
from dataclasses import dataclass

from kanwoo.chapter.models import Chapter
from kanwoo.manga.models import Manga
from kanwoo.translation.models import Translation
from .entities import ReadingStartTypeEnum

@dataclass
class CreateReadingProgressDTO:
    chapter: Chapter
    page: Optional[int]

@dataclass
class UpdateReadingSessionDTO:
    chapter_id: int
    page: int
    is_finished: bool

@dataclass
class UpdateHistoryItemDTO:
    page: int

@dataclass
class CreateHistoryItemDTO:
    chapter_id: int
    session_id: int
    page: int

@dataclass
class ReadingHistoryContextDTO:
    chapter: Optional[Chapter]
    manga: Optional[Manga]
    translation: Optional[Translation]

@dataclass
class ReadingBookmarkContextDTO:
    chapter: Optional[Chapter]
    manga: Optional[Manga]

@dataclass
class ReadingSaveDTO:
    id: int
    chapter: Chapter
    manga: Manga
    page: int
    is_finished: bool


@dataclass
class ChapterProgressDTO:
    page: int

@dataclass
class ReadingStartDTO:
    start_type: ReadingStartTypeEnum
    chapter: Optional[Chapter]