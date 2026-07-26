from .dto import SettingsSecurityDTO

class SettingsService:

    def user_get_security_settings(self, current_user):
        return SettingsSecurityDTO(
            password_auth_enabled=current_user.has_password_auth,
            yandex_oauth_enabled=current_user.has_yandex_oauth
        )
