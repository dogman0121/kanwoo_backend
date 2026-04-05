from dataclasses import dataclass


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
    manga_slug: str

@dataclass
class CollectionRemoveMangaDTO:
    manga_slug: str