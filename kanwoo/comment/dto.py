from typing import Optional, List, Dict
from dataclasses import dataclass

from .models import Comment

@dataclass
class CreateCommentDTO:
    text: str

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

@dataclass
class SubthreadContextDTO:
    root_comment: CommentContextDTO
    discussion: List[CommentContextDTO]