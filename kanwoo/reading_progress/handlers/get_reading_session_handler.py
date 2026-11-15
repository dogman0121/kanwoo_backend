from flask import request
from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer, respond
from kanwoo.exceptions import ApiBadRequest
from kanwoo.translation.services import TranslationService
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingSessionService

@profile_required()
@inject
def get_reading_session_handler(
    current_profile,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
    rs_service: ReadingSessionService = Provide[AppContainer.reading_progress_container.reading_session_service]
):
    translation_id = request.args.get("translation_id")

    if not translation_id:
        raise ApiBadRequest(detail={"translation_id": ["Translation id is required."]})

    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)
    
    reading_session = rs_service.user_get_reading_session(current_profile, translation)

    return respond(data={"id": reading_session.id})