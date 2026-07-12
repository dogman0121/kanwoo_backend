from dataclasses import dataclass
from typing import Optional

@dataclass
class AuthRegisterDTO:
    code: str
    email: str
    password: str

@dataclass
class AuthLoginDTO:
    email: str
    password: str

@dataclass
class AuthRecoveryDTO:
    token: str
    new_password: str


@dataclass
class AuthYandexOauthDTO:
    access_token: str
    expires_in: str
    extra_data: str
    token_type: str

@dataclass
class AuthYandexOauthUserDTO:
    login: str
    id: str
    is_avatar_empty: bool
    default_avatar_id: Optional[str]