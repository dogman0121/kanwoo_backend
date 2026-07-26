from typing import Optional
from dataclasses import dataclass

@dataclass
class CommentCreateDTO:
    text: str
    parent_id: Optional[int]
    manga_id: Optional[int]
    chapter_id: Optional[int]