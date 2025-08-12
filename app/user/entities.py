from dataclasses import dataclass
from typing import Optional


@dataclass
class UserEntity:
    id: Optional[int]
    login: str
    email: str
    password: str
    is_verified: bool