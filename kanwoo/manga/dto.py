from dataclasses import dataclass
from typing import List, Optional
from kanwoo.entity import File, FileAction


@dataclass
class NameTranslationDTO:
    lang_id: int
    name: str

@dataclass
class MangaCreateDTO:
    slug: Optional[str]
    name: str
    name_translations: Optional[List[NameTranslationDTO]]
    description: str
    type_id: int
    status_id: int
    adult_id: int
    year: int
    privacy_id: int
    genres_id: Optional[List[int]]
    poster: Optional[File]
    background: Optional[File]
    author_id: Optional[int]
    promo_name: Optional[File]
    promo_background: Optional[File]
    promo_logo: Optional[File]


@dataclass
class MangaUpdateDTO:
    slug: str
    name: str
    description: str
    type_id: int
    status_id: int
    adult_id: int
    year: int
    privacy_id: int
    name_translations: Optional[List[NameTranslationDTO]]
    genres_id: Optional[List[int]]
    poster: Optional[File]
    background: Optional[File]
    poster_action: FileAction
    background_action: FileAction
    promo_name: Optional[File]
    promo_background: Optional[File]
    promo_logo: Optional[File]
    promo_name_action: FileAction
    promo_background_action: FileAction
    promo_logo_action: FileAction

@dataclass
class MangaSuggestionCreateDTO:
    name: str
    link: str
    comment: Optional[str]
    creator_id: Optional[int]