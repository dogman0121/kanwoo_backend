from dependency_injector.wiring import inject, Provide

from kanwoo import respond, AppContainer
from kanwoo.profile.middleware import profile_required
from kanwoo.translation.services import TranslationService
from kanwoo.translation.schemas import GetTranslationSchemaFull, GetTranslationContextSchema

@profile_required(optional=True)
@inject
def get_translation_handler(
    current_profile,
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    translation_context = translation_service.user_get_translation_context(current_profile, translation)

    return respond(
        data=GetTranslationSchemaFull().dump(translation),
        context=GetTranslationContextSchema().dump(translation_context)
    )