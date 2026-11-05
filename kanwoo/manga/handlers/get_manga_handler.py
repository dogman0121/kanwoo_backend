from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.logs import log_runtime
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaService
from kanwoo.manga.schemas import GetMangaContextSchema, GetMangaSchemaFull

@log_runtime
@profile_required(optional=True)
@inject
def get_manga_handler(
    current_profile, 
    manga_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug, by_link=True)

    manga_context = manga_service.user_get_manga_context(current_profile, manga)

    return respond(
        data=GetMangaSchemaFull().dump(manga), 
        context=GetMangaContextSchema().dump(manga_context),
        status_code=200
    )