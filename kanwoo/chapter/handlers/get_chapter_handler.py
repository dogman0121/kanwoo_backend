from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from kanwoo.chapter.services import ChapterPublicService, ChapterContextService
from kanwoo.chapter.schemas import (
    GetChapterSchemaFull, 
    GetChapterContextSchema
)

@profile_required(optional=True)
@inject
def get_chapter_handler(
    current_profile, 
    chapter_id,
    chapter_public_service: ChapterPublicService = Provide[AppContainer.chapter_container.chapter_public_service],
    chapter_context_service: ChapterContextService = Provide[AppContainer.chapter_container.chapter_context_service]
):
    chapter = chapter_public_service.get_chapter_by_id(chapter_id)

    chapter_context = chapter_context_service.get(
        current_profile,
        chapter,
        include_translation=True
    )

    return respond(
        data=GetChapterSchemaFull().dump(chapter), 
        context=GetChapterContextSchema().dump(chapter_context)
    )