from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond

from kanwoo.profile.middleware import profile_required
from kanwoo.translation.services import TranslationService
from kanwoo.chapter.services import ChapterService
from kanwoo.studio.schemas import GetStudioChapterSchema

@profile_required()
@inject
def get_translations_chapters_handler(
    current_profile,
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    chapters = chapter_service.user_get_translation_chapters(current_profile, translation)

    return respond(
        data=GetStudioChapterSchema(many=True).dump(chapters)
    )