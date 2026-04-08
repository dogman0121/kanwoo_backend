from dataclasses import dataclass

@dataclass
class UserCreateDTO:
    email: str
    password_hash: str