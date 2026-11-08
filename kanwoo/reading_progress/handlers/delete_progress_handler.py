from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingProgressService

@profile_required()
@inject
def delete_progress_handler(
    current_profile,
    progress_id,
    rp_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service]
):
    rp_service.user_delete_progress_save(current_profile, progress_id)

    return respond(data={"success": True})