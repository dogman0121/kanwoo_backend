from typing import Optional, List

from kanwoo.entity import File

from dataclasses import dataclass

@dataclass
class TranslationChapterCreateDTO:
    chapter: int
    privacy: int
    name: Optional[str]
    pages: List[File]
    pages_order: List[str]

@dataclass
class TranslationCreateDTO:
    name: str
    lang_id: int
    privacy_id: int
    is_official: bool

@dataclass
class TranslationUpdateDTO:
    name: str
    privacy: int