from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer, respond
from kanwoo.exceptions import ApiForbidden
from kanwoo.entity import Privacy
from kanwoo.profile.middleware import profile_required
from kanwoo.translation.services import TranslationService
from kanwoo.chapter.services import ChapterService
from kanwoo.studio.schemas import GetStudioCreateChapterFormSchema


@profile_required()
@inject
def get_create_chapter_form_handler(
    current_profile,
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    if not translation_service.translation_policy.can_edit(current_profile, translation):
        raise ApiForbidden()

    last_chapter_number = chapter_service.user_get_translation_last_chapter_number(current_profile, translation_id)

    return respond(
        GetStudioCreateChapterFormSchema().dump({
            "name": "",
            "chapter": last_chapter_number + 1,
            "extra_number": None,
            "privacy_id": Privacy.PRIVATE,
            "pages": [],
            "blocked_fields": []
        })
    )