from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingBookmarkService

@profile_required()
@inject
def delete_bookmark_handler(
    current_profile,
    bookmark_id,
    rb_service: ReadingBookmarkService = Provide[AppContainer.reading_progress_container.reading_bookmark_service]
):
    rb_service.delete_reading_bookmark(current_profile, bookmark_id)

    return respond(data={"success": True})