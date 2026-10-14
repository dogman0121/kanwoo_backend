from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond

from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaService
from kanwoo.translation.services import TranslationService
from kanwoo.studio.schemas import GetStudioTranslationSchema

@profile_required()
@inject
def get_manga_translations_handler(
    current_profile,
    manga_slug,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    translations = translation_service.user_get_manga_translations(current_profile, manga, official=True)

    return respond(
        data=GetStudioTranslationSchema(many=True).dump(translations)
    )