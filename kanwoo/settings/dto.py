from dataclasses import dataclass


@dataclass
class SettingsSecurityDTO:
    password_auth_enabled: bool
    yandex_oauth_enabled: bool