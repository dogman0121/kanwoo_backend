from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required
from kanwoo.chapter.services import ChapterService
from kanwoo.studio.schemas import GetStudioChapterSchema

@profile_required()
@inject
def get_chapter_handler(
    current_profile,
    chapter_id,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):
    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id)

    return respond(
        data=GetStudioChapterSchema().dump(chapter)
    )