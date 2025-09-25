from dataclasses import dataclass
from typing import Optional

from app.entity import File

@dataclass
class TeamCreateDTO:
    name: str
    about: Optional[str]
    poster: Optional[File]