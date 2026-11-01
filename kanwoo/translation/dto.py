from typing import Optional, List, Dict

from kanwoo.entity import File
from kanwoo.manga.models import Manga
from kanwoo.translation.entities import ReadingModeEnum

from dataclasses import dataclass

@dataclass
class CreateTranslationDTO:
    name: str
    lang_id: int
    privacy_id: int
    is_official: bool

@dataclass
class UpdateTranslationDTO:
    name: str
    privacy_id: int
    default_reading_mode_id: ReadingModeEnum

@dataclass
class TranslationListContextDTO:
    viewer: Dict[int, Dict[str, str]] 

@dataclass
class TranslationContextDTO:
    viewer: Dict[str, str]
    manga: Optional[Manga]