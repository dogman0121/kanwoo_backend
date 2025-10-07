from dataclasses import dataclass
from typing import Optional, List

from app.entity import File

@dataclass
class TeamCreateDTO:
    name: str
    about: Optional[str]
    avatar: Optional[File]


@dataclass
class TeamLinkDTO:
    name: str
    link: str

@dataclass
class TeamUpdateDTO:
    name: str
    slug: str
    about: Optional[str]
    avatar: Optional[File]
    avatar_action: str
    links: Optional[List[TeamLinkDTO]]