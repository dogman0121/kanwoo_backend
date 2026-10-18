from dependency_injector.wiring import inject, Provide
from flask import request

from kanwoo import AppContainer
from kanwoo.exceptions import ApiBadRequest
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.profile.services import ProfileService
from kanwoo.manga.services import MangaService
from kanwoo.translation.services import TranslationService
from kanwoo.translation.schemas import GetTranslationContextSchema
from kanwoo.studio.schemas import GetTranslationSchemaFull


@profile_required()
@inject
def get_profile_translations_list_handler(
    current_profile,
    profile_slug,
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    translations_list = translation_service.user_get_profile_translations(current_profile, profile)

    translations_contexts = [translation_service.user_get_translation_context(current_profile, t) for t in translations_list]

    return respond(
        data=GetTranslationSchemaFull(many=True).dump(translations_list),
        context=GetTranslationContextSchema(many=True).dump(translations_contexts)
    )