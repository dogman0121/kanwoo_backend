from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond

from kanwoo.profile.middleware import profile_required
from kanwoo.translation.services import TranslationService
from kanwoo.studio.schemas import GetStudioTranslationSchema

@profile_required()
@inject
def get_translation_handler(
    current_profile,
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    return respond(
        data=GetStudioTranslationSchema().dump(translation)
    )