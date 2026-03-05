from dependency_injector import containers, providers

from .repositories import SearchRepository
from .services import SearchService

class SearchContainer(containers.DeclarativeContainer):

    db_session = providers.Dependency()

    search_repo = providers.Singleton(
        SearchRepository,
        db_session=db_session
    )

    search_service = providers.Factory(
        SearchService,
        search_repo=search_repo
    )