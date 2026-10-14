from dataclasses import dataclass
from typing import List, Optional
from kanwoo.entity import File, FileAction


@dataclass
class NameTranslationDTO:
    lang_id: int
    name: str

@dataclass
class CreateMangaDTO:
    name: str
    description: str
    type_id: int
    status_id: int
    adult_id: int
    year: int
    privacy_id: int
    slug: Optional[str] = None
    name_translations: Optional[List[NameTranslationDTO]] = None
    genres_ids: Optional[List[int]] = None
    poster: Optional[File] = None
    background: Optional[File] = None
    promo_name: Optional[File] = None
    promo_background: Optional[File] = None
    promo_logo: Optional[File] = None


@dataclass
class UpdateMangaDTO:
    slug: str
    name: str
    description: str
    type_id: int
    status_id: int
    adult_id: int
    year: int
    privacy_id: int
    name_translations: Optional[List[NameTranslationDTO]]
    genres_ids: Optional[List[int]]
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