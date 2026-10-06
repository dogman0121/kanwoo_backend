from typing import Optional, List, Dict
from dataclasses import dataclass

from .models import Comment

@dataclass
class CreateCommentDTO:
    text: str
    parent_id: Optional[int]
    manga_id: Optional[int]
    chapter_id: Optional[int]


@dataclass
class CommentViewerContextDTO:
    vote: int

@dataclass
class CommentContextDTO:
    viewer: CommentViewerContextDTO

@dataclass
class SubthreadDTO:
    root_comment: Comment
    discussion: List[Comment]
    discussion_pagination: Dict
