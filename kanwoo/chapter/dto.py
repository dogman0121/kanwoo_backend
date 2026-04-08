from typing import Optional, List

from dataclasses import dataclass

from kanwoo.entity import File

@dataclass
class ChapterCreateDTO:
    chapter: int
    privacy: int
    name: Optional[str]
    pages: List[File]
    pages_order: List[str]

@dataclass
class ChapterUpdateDTO:
    chapter: int
    privacy: int
    name: Optional[str]
    pages: List[File]
    pages_order: List[str]