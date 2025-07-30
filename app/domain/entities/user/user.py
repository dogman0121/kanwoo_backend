from dataclasses import dataclass

@dataclass
class User:
    id: int
    uuid: str
    avatar: str
    login: str
    email: str
    password: str
    role: int