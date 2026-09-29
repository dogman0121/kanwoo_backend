from typing import Optional, List, Dict

from dataclasses import dataclass

from kanwoo.entity import File
from kanwoo.manga.models import Manga
from kanwoo.translation.models import Translation

@dataclass
class ChapterCreateDTO:
    chapter: int
    privacy: int
    name: Optional[str]
    pages: List[File]
    pages_order: List[str]

@dataclass
class ChapterUpdateDTO:
    chapter: int
    privacy: int
    name: Optional[str]
    pages: List[File]
    pages_order: List[str]

@dataclass
class ChapterMetadataDTO:
    pages: List[Dict[str, int]]

@dataclass
class ChapterContextDTO:
    manga: Manga
    translation: Translation