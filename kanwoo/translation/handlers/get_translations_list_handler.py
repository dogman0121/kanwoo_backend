from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import respond, AppContainer
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaService
from kanwoo.translation.services import MangaTranslationService, TranslationService
from kanwoo.translation.schemas import GetTranslationSchemaFull, GetTranslationContextSchema

@profile_required(optional=True)
@inject
def get_translations_list_handler(
    current_profile,
    manga_translation_service: MangaTranslationService = Provide[AppContainer.translation_container.manga_translation_service],
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    if "manga_id" in request.args:
        translations = manga_translation_service.get(request.args.get("manga_id"))
    else:
        raise NotImplementedError()

    translation_context = [translation_service.user_get_translation_context(current_profile, t) for t in translations]

    return respond(
        data=GetTranslationSchemaFull().dump(translations, many=True),
        context=GetTranslationContextSchema().dump(translation_context, many=True)
    )