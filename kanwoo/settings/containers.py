from dependency_injector import containers, providers
from .services import SettingsService

class SettingsContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    settings_service = providers.Factory(
        SettingsService
    )