from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required
from kanwoo.chapter.dto import CreateChapterDTO
from kanwoo.chapter.services import ChapterService
from kanwoo.translation.services import TranslationService
from kanwoo.studio.schemas import CreateStudioChapterSchema, GetStudioChapterSchema

@profile_required()
@inject
def create_chapter_handler(
    current_profile,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):

    create_schema = CreateStudioChapterSchema().load({
        "name": request.form.get("name"),
        "chapter": request.form.get("chapter"),
        "privacy_id": request.form.get("privacy_id"),
        "pages": request.files.get("files"),
        "pages_order": request.form.get("pages_order")
    })

    translation = translation_service.user_get_translation_by_id(current_profile, create_schema.get("translation_id"))

    create_dto = CreateChapterDTO(
        name=create_schema.get("name"),
        chapter=create_schema.get("chapter"),
        privacy_id=create_schema.get("privacy_id"),
        pages=create_schema.get("pages"),
        pages_order=create_schema.get("pages_order")
    )

    chapter = chapter_service.user_create_chapter(current_profile, translation, create_dto)

    return respond(
        data=GetStudioChapterSchema().dump(chapter)
    )