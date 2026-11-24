from dependency_injector.wiring import inject, Provide
from marshmallow.experimental.context import Context

from kanwoo import AppContainer, respond
from kanwoo.logs import log_runtime
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaService, MangaPublicService, MangaContextService, MangaStatService
from kanwoo.manga.schemas import GetMangaContextSchema, GetMangaSchemaFull

@log_runtime
@profile_required(optional=True)
@inject
def get_manga_handler(
    current_profile, 
    manga_slug,
    manga_public_service: MangaPublicService = Provide[AppContainer.manga_container.manga_public_service],
    manga_context_service: MangaContextService = Provide[AppContainer.manga_container.manga_context_service],
    manga_stat_service: MangaStatService = Provide[AppContainer.manga_container.manga_stat_service]
):
    manga = manga_public_service.get_manga_by_slug(manga_slug)
    manga_stats = manga_stat_service.get(manga_slug)
    manga_context = manga_context_service.get(current_profile, manga)

    with Context({"stats": manga_stats}):
        return respond(
            data=GetMangaSchemaFull().dump(manga), 
            context=GetMangaContextSchema().dump(manga_context),
            status_code=200
        )