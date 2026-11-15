from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaPublicService
from kanwoo.reading_progress.services import MangaReadingStartService
from kanwoo.reading_progress.schemas import GetReadingBookmarkSchema, GetReadingBookmarkContextSchema

@profile_required()
@inject
def get_manga_bookmark_handler(
    current_profile,
    manga_slug,
    manga_service: MangaPublicService = Provide[AppContainer.manga_container.manga_public_service],
    manga_reading_start_service: MangaReadingStartService = Provide[AppContainer.reading_progress_container.manga_reading_start_service] 
):
    manga = manga_service.get_manga_by_slug(manga_slug)

    chapter = manga_reading_start_service.get(current_profile, manga)

    return respond(
    )