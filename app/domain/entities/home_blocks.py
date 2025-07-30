from dataclasses import dataclass

from typing import List

from app.domain.entities.manga.manga import Manga


@dataclass
class HomeBlocks:
    slides: List[Manga]
    newest: List[Manga]
    ended: List[Manga]
    most_viewed: List[Manga]
