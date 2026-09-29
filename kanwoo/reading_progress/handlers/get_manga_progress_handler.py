from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.reading_progress.schemas import GetReadingProgressContextSchema, GetReadingProgressSchema

@profile_required()
@inject
def get_manga_progress_handler(
    current_profile,
    manga_slug,
    rp_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service]
):

    progress = rp_service.user_get_manga_progress(current_profile, manga_slug)
    progress_context = rp_service.user_get_progress_context(current_profile, progress, include_chapter=True)

    return respond(
        data=GetReadingProgressSchema().dump(progress),
        context=GetReadingProgressContextSchema().dump(progress_context)
    )