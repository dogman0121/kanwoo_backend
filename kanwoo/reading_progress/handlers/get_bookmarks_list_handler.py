from typing import TYPE_CHECKING
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from kanwoo.reading_progress.services import ReadingBookmarkService
from kanwoo.reading_progress.schemas import GetReadingBookmarkContextSchema, GetReadingBookmarkSchema

@profile_required()
@inject
def get_bookmarks_list_handler(
    current_profile,
    rb_service: ReadingBookmarkService = Provide[AppContainer.reading_progress_container.reading_bookmark_service]
):
    bookmarks = rb_service.user_get_profile_reading_bookmarks(current_profile)
    bookmarks_contexts = [
        rb_service.user_get_reading_bookmark_context(
            current_profile, 
            b,
            include_manga=True,
            include_chapter=True
        ) for b in bookmarks
    ]

    return respond(
        data=GetReadingBookmarkSchema().dump(bookmarks, many=True),
        context=GetReadingBookmarkContextSchema().dump(bookmarks_contexts, many=True)
    )
