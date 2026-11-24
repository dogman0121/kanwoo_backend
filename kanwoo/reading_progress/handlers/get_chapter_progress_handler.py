from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ChapterProgressService
from kanwoo.reading_progress.schemas import GetChapterProgressSchema

@profile_required()
@inject
def get_chapter_progress_handler(
    current_profile,
    chapter_id,
    chapter_progress_service: ChapterProgressService = Provide[AppContainer.reading_progress_container.chapter_progress_service]
):
    progress = chapter_progress_service.get(current_profile, chapter_id)

    return respond(
        data=GetChapterProgressSchema().dump(progress)
    )