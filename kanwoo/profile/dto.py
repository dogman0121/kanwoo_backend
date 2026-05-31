from dataclasses import dataclass
from typing import Optional, List

from kanwoo.entity import File

@dataclass
class ProfileCreateDTO:
    name: str
    slug: str
    about: Optional[str]
    avatar: Optional[File]
    creator_id: Optional[int]
    owner_id: Optional[int]


@dataclass
class ProfileLinkDTO:
    name: str
    link: str

@dataclass
class ProfileUpdateDTO:
    name: str
    slug: str
    about: Optional[str]
    avatar: Optional[File]
    avatar_action: str
    links: Optional[List[ProfileLinkDTO]]