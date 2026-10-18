from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required
from kanwoo.profile.services import ProfileService
from kanwoo.manga.services import MangaService
from kanwoo.translation.services import TranslationService
from kanwoo.translation.dto import UpdateTranslationDTO
from kanwoo.studio.schemas import UpdateStudioTranslationSchema, GetStudioTranslationSchema

@profile_required()
@inject
def update_translation_handler(
    current_profile, 
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    update_data = UpdateStudioTranslationSchema().load(request.form)

    update_dto = UpdateTranslationDTO(
        name=update_data.get("name"),
        privacy=update_data.get("privacy")
    )

    updated_translation = translation_service.user_update_translation(current_profile, translation, update_dto)

    return respond(data=GetStudioTranslationSchema().dump(updated_translation))