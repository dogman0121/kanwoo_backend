from typing import List, Optional
from dataclasses import dataclass

@dataclass
class SearchMangaDTO:
    query: Optional[str]
    genres: Optional[List[int]]
    types: Optional[List[int]]
    adults: Optional[List[int]]
    statuses: List[int]
    year_from: Optional[int]
    year_to: Optional[int]