from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.reading_progress.schemas import GetReadingProgressSchema, GetReadingProgressContextSchema

@profile_required()
@inject
def get_chapter_progress_handler(
    current_profile,
    chapter_id,
    rp_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service],
):
    progress = rp_service.user_get_chapter_progress(current_profile, chapter_id)
    progress_context = rp_service.user_get_progress_context(current_profile, progress)

    return respond(
        data=GetReadingProgressSchema().dump(progress),
        context=GetReadingProgressContextSchema().dump(progress_context)
    )