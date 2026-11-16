from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaStatService

@inject
def add_view_handler(
    manga_slug,
    manga_stat_service: MangaStatService = Provide[AppContainer.manga_container.manga_stat_service],
):
    manga_stat_service.add_view(manga_slug)


    return respond(data={"success": True})