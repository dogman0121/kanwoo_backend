from dataclasses import dataclass
from typing import Optional

@dataclass
class UserCreateDTO:
    email: Optional[str]
    password_hash: Optional[str]