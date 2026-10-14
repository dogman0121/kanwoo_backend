from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required
from kanwoo.profile.services import ProfileService
from kanwoo.manga.services import MangaService
from kanwoo.translation.services import TranslationService
from kanwoo.translation.dto import CreateTranslationDTO
from kanwoo.studio.schemas import CreateStudioTranslationSchema, GetStudioTranslationSchema

@profile_required()
@inject
def create_translation_handler(
    current_profile,
    profile_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service]
):
    create_schema = CreateStudioTranslationSchema().load(request.json)

    manga = manga_service.user_get_manga_by_id(current_profile, create_schema["manga"])

    create_dto = CreateTranslationDTO(
        name=create_schema["name"],
        privacy_id=create_schema["privacy"],
        lang_id=1,
        is_official=False
    )
    author = profile_service.user_get_profile_by_slug(profile_slug)

    translation = translation_service.user_create_manga_translation(current_profile, author, manga, create_dto)

    return respond(data=GetStudioTranslationSchema().dump(translation))