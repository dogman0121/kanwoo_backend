from flask import request
from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.exceptions import ApiBadRequest
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingHistoryService
from kanwoo.reading_progress.schemas import DeleteReadingHistorySchema, DeleteReadingHistoryModeEnum

@profile_required()
@inject
def delete_history_handler(
    current_profile,
    rh_service: ReadingHistoryService = Provide[AppContainer.reading_progress_container.reading_history_service]
):

    delete_schema = DeleteReadingHistorySchema().load()

    mode = delete_schema.get("mode")
    history_ids = delete_schema.get("history_ids")

    if mode == DeleteReadingHistoryModeEnum.ALL:
        rh_service.user_delete_all_history(current_profile)
    elif mode == DeleteReadingHistoryModeEnum.SELECTED:
        rh_service.user_delete_selected_history(current_profile, history_ids)
    else:
        raise ApiBadRequest(error="bad_request", detail = {mode: ["The mode must be all or selected."]})

    return respond(data={"success": True})