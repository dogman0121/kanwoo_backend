from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import respond, AppContainer
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaService
from kanwoo.translation.services import TranslationService
from kanwoo.translation.schemas import GetTranslationSchemaFull, GetTranslationContextSchema

@profile_required(optional=True)
@inject
def get_translations_list_handler(
    current_profile,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    if "manga_id" in request.args:
        manga = manga_service.user_get_manga_by_slug(current_profile, request.args.get("manga_id"))

        translations = translation_service.user_get_manga_translations(current_profile, manga)
    else:
        raise NotImplementedError()

    translation_context = [translation_service.user_get_translation_context(current_profile, t) for t in translations]

    return respond(
        data=GetTranslationSchemaFull().dump(translations, many=True),
        context=GetTranslationContextSchema().dump(translation_context, many=True)
    )