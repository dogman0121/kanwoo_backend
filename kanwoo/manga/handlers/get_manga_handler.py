from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.logs import log_runtime
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaService, MangaPublicService, MangaContextService
from kanwoo.manga.schemas import GetMangaContextSchema, GetMangaSchemaFull

@log_runtime
@profile_required(optional=True)
@inject
def get_manga_handler(
    current_profile, 
    manga_slug,
    manga_public_service: MangaPublicService = Provide[AppContainer.manga_container.manga_public_service],
    manga_context_service: MangaContextService = Provide[AppContainer.manga_container.manga_context_service]
):
    manga = manga_public_service.get_manga_by_slug(manga_slug)

    manga_context = manga_context_service.get(current_profile, manga)

    return respond(
        data=GetMangaSchemaFull().dump(manga), 
        context=GetMangaContextSchema().dump(manga_context),
        status_code=200
    )