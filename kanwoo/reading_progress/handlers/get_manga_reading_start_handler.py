from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required

from kanwoo.manga.services import MangaPublicService
from kanwoo.reading_progress.services import MangaReadingStartService
from kanwoo.reading_progress.schemas import GetReadingStartSchema

@profile_required(optional=True)
@inject
def get_manga_reading_start_handler(
    current_profile,
    manga_slug,
    manga_public_service: MangaPublicService = Provide[AppContainer.manga_container.manga_public_service],
    manga_reading_start_service: MangaReadingStartService = Provide[AppContainer.reading_progress_container.manga_reading_start_service]
):
    manga = manga_public_service.get_manga_by_slug(manga_slug)

    reading_start = manga_reading_start_service.get(current_profile, manga)

    return respond(
        data=GetReadingStartSchema().dump(reading_start)
    )