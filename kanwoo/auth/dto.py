from dataclasses import dataclass

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