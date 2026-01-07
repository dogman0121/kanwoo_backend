from dataclasses import dataclass
from typing import List, Dict
from app.entity import File, FileAction

@dataclass
class NameTranslationDTO:
    lang: str
    name: str

@dataclass
class MangaCreateDTO:
    name: str


@dataclass
class MangaUpdateDTO:
    slug: str
    name: str
    description: str
    type: int
    status: int
    adult: int
    year: int
    name_translations: List[NameTranslationDTO]
    genres: List[int]
    poster: File
    background: File
    poster_action: FileAction
    background_action: FileAction
    promo_name: File
    promo_background: File
    promo_logo: File
    promo_name_action: FileAction
    promo_background_action: FileAction
    promo_logo_action: FileAction
