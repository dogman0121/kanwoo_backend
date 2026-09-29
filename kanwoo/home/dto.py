from typing import Union, Optional
from dataclasses import dataclass

from .entities import HeroBlockType, HomeBlockType


@dataclass
class HeroMangaDataDTO:
    slug: str
    logo: str
    background: str
    name: str

@dataclass
class HeroAddDTO:
    logo: str
    background: str
    link: str

@dataclass
class HeroBlockDTO:
    type: HeroBlockType
    data: Union[HeroMangaDataDTO]


@dataclass
class HomeMapItemDTO:
    type: HomeBlockType
    hash: Optional[str]
    title: str