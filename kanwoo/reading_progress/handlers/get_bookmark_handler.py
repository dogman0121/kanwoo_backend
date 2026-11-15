from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingBookmarkService
from kanwoo.reading_progress.schemas import GetReadingBookmarkSchema, GetReadingBookmarkContextSchema

@profile_required()
@inject
def get_bookmark_handler(
    current_profile,
    bookmark_id,
    rb_service: ReadingBookmarkService = Provide[AppContainer.reading_progress_container.reading_bookmark_service]
):

    bookmark = rb_service.user_get_reading_bookmark_by_id(current_profile, bookmark_id)
    bookmark_context = rb_service.user_get_reading_bookmark_context(
        current_profile, 
        bookmark,
        include_manga=True,
        include_chapter=True
    )

    return respond(
        data=GetReadingBookmarkSchema().dump(bookmark),
        context=GetReadingBookmarkContextSchema().dump(bookmark_context)
    )