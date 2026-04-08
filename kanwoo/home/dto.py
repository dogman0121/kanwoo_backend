from typing import Union
from dataclasses import dataclass

from .schemas import HeroBlockType


@dataclass
class HeroMangaDataDTO:
    slug: str
    logo: str
    background: str
    name: str

@dataclass
class HeroBlockDTO:
    type: HeroBlockType
    data: Union[HeroMangaDataDTO]

