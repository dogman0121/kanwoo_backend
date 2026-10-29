from typing import Union, Optional, List
from dataclasses import dataclass

from kanwoo.chapter.models import Chapter
from kanwoo.manga.models import Manga
from .entities import HeroBlockType, HomeBlockType


@dataclass
class HeroMangaDataDTO:
    slug: str
    logo: str
    background: str
    name: str

@dataclass
class HeroBlockDTO:
    type: HeroBlockType
    data: Union[HeroMangaDataDTO]

@dataclass
class ReadingProgressDTO:
    id: int
    page: int
    chapter: Chapter
    manga: Manga

@dataclass
class LastAddedChaptersDTO:
    chapters: List[Chapter]
    pagination: dict

@dataclass
class HomeMapItemDTO:
    type: HomeBlockType
    hash: Optional[str]
    title: str