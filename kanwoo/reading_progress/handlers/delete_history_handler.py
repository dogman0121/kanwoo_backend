from flask import request
from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.exceptions import ApiBadRequest
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.reading_progress.schemas import DeleteReadingProgressSchema

@profile_required()
@inject
def delete_history_handler(
    current_profile,
    rp_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service]
):

    delete_schema = DeleteReadingProgressSchema().load()

    mode = delete_schema.get("mode")
    progresses_ids = delete_schema.get("progresses_ids")

    if mode == "all":
        rp_service.user_delete_all_history(current_profile)
    elif mode == "selected":
        rp_service.user_delete_many_progresses(current_profile, progresses_ids)
    else:
        raise ApiBadRequest(error="bad_request", detail = {mode: ["The mode must be all or selected."]})

    return "", 204