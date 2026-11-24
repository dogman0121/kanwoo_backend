from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required
from kanwoo.profile.services import ProfileService
from kanwoo.manga.services import MangaService
from kanwoo.translation.services import TranslationService
from kanwoo.translation.dto import CreateTranslationDTO
from kanwoo.studio.schemas import CreateStudioMangaTranslationSchema, GetStudioTranslationSchema

@profile_required()
@inject
def create_manga_translation_handler(
    current_profile,
    manga_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
):
    create_schema = CreateStudioMangaTranslationSchema().load(request.json)

    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    create_dto = CreateTranslationDTO(
        name=create_schema["name"],
        privacy_id=create_schema["privacy_id"],
        lang_id=create_schema["lang_id"],
        is_official=True
    )

    translation = translation_service.user_create_manga_translation(current_profile, current_profile, manga, create_dto)

    return respond(data=GetStudioTranslationSchema().dump(translation))