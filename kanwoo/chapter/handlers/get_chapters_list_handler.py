from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.translation.services import TranslationService

from kanwoo.chapter.services import ChapterService
from kanwoo.chapter.schemas import (
    GetChapterSchemaFull, 
    GetChapterContextSchema
)

@profile_required(optional=True)
@inject
def get_chapters_list_handler(
    current_profile,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):
    if "translation_id" in request.args:
        translation = translation_service.user_get_translation_by_id(current_profile, request.args.get("translation_id"))

        chapters = chapter_service.user_get_translation_chapters(current_profile, translation)
    else:
        raise NotImplementedError()

    chapter_context = [chapter_service.user_get_chapter_context(c, current_profile) for c in chapters]

    return respond(
        data=GetChapterSchemaFull().dump(chapters, many=True), 
        context=GetChapterContextSchema().dump(chapter_context, many=True)
    )