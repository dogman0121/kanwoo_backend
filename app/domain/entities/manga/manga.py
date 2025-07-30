from dataclasses import dataclass
from typing import List

from app.domain.entities.manga import Genre
from app.domain.entities.user import User


@dataclass
class Manga:
    id: int
    slug: str
    description: str
    name: str
    year: int
    views: int
    genres: List[Genre]
    verified: bool
    creator: User
    authors: List[User]
    artists: List[User]
    publishers: List[User]

    def __post_init__(self):
        if self.verified is None:
            self.verified = False

        if self.views is None:
            self.views = 0