from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.middleware import pagination
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.chapter.services import ChapterService
from kanwoo.chapter.schemas import GetChapterSchemaMini, GetChapterContextSchema


@profile_required(optional=True)
@pagination
@inject
def get_last_added_chapters_handler(
    current_profile,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
    cursor = None
):

    chapters, cursor, has_more = chapter_service.user_get_last_added_chapters(current_profile, cursor)

    chapters_contexts = [chapter_service.user_get_chapter_context(chap) for chap in chapters]

    return respond(
        data=GetChapterSchemaMini().dump(chapters, many=True),
        context=GetChapterContextSchema().dump(chapters_contexts, many=True),
        cursor=cursor,
        has_more=has_more
    )
