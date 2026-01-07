from typing import Optional, List

from dataclasses import dataclass

from app.entity import File

@dataclass
class ChapterCreateDTO:
    chapter: int
    tome: int
    name: Optional[str]
    pages: List[File]
    pages_order: List[str]
