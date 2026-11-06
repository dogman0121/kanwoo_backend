from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.reading_progress.schemas import GetReadingProressSaveSchema
from kanwoo.manga.services import MangaService

@profile_required()
@inject
def get_manga_progress_handler(
    current_profile,
    manga_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
    rp_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    progress = rp_service.user_get_manga_progress(current_profile, manga.id)

    return respond(
        data=GetReadingProressSaveSchema().dump(progress)
    )