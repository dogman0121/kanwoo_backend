from flask import request
from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.reading_progress.schemas import UpdateReadingProgressSchema
from kanwoo.reading_progress.dto import UpdateReadingProgressDTO


@profile_required()
@inject
def update_progress_handler(
    current_profile,
    progress_id,
    rp_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service], 
):

    update_schema = UpdateReadingProgressSchema().load(request.json)

    progress = rp_service.user_get_progress_by_id(current_profile, progress_id)

    update_dto = UpdateReadingProgressDTO(
        page=update_schema.get("page")
    )
    
    rp_service.user_update_progress(current_profile, progress, update_dto)

    return respond(data={"success": True})