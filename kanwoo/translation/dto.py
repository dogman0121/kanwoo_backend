from typing import Optional, List, Dict

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

@dataclass
class TranslationListContextDTO:
    viewer: Dict[int, Dict[str, str]] 

@dataclass
class TranslationContextDTO:
    viewer: Dict[str, str]