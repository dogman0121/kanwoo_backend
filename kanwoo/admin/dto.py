from dataclasses import dataclass
from typing import List, Optional

from kanwoo.entity import FileAction, File
from kanwoo.manga.dto import NameTranslationDTO


@dataclass
class AdminMainDashboardDTO:
    manga_reports_count: int
    chapters_reports_count: int
    manga_waiting_moderation_count: int
    chapter_waiting_moderation_count: int
    manga_sugesstions_count: int
    feedback_messages_count: int

@dataclass
class AdminMangaCreateDTO:
    slug: Optional[str]
    name: str
    name_translations: Optional[List[NameTranslationDTO]]
    description: str
    type_id: int
    status_id: int
    adult_id: int
    year: int
    privacy_id: int
    genres_ids: Optional[List[int]]
    poster: Optional[File]
    background: Optional[File]
    promo_name: Optional[File]
    promo_background: Optional[File]
    promo_logo: Optional[File]


@dataclass
class AdminMangaUpdateDTO:
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
    author_id: int


@dataclass
class AdminMangaFiltersDTO:
    query: str
    statuses: List[str]

@dataclass
class AdminProfileFiltersDTO:
    query: str