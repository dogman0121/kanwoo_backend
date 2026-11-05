from dataclasses import dataclass
from typing import Optional

@dataclass
class CollectionCreateDTO:
    name: str
    privacy_id: int

@dataclass
class CollectionUpdateDTO:
    name: str
    description: str
    privacy_id: int


@dataclass
class CollectionAddMangaDTO:
    manga_id: str

@dataclass
class CollectionRemoveMangaDTO:
    manga_id: str


@dataclass
class CollectionViewerContextDTO:
    is_saved: bool

@dataclass
class CollectionContextDTO:
    viewer: Optional[CollectionViewerContextDTO]