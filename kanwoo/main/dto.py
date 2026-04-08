from typing import List
from dataclasses import dataclass

@dataclass
class MetaMainDTO:
    languages: List["Language"]
    privacies: List["Privacy"]

@dataclass
class MetaMangaDTO:
    genres: List["Genre"]
    statuses: List["Status"]
    types: List["Type"]
    adults: List["Adult"]

@dataclass
class MetaDTO:
    main: MetaMainDTO
    manga: MetaMangaDTO

@dataclass
class FeedbackCreateDTO:
    message: str