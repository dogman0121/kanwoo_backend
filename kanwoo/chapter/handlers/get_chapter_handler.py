from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from kanwoo.chapter.services import ChapterService
from kanwoo.chapter.schemas import (
    GetChapterSchemaFull, 
    GetChapterContextSchema
)

@profile_required(optional=True)
@inject
def get_chapter_handler(
    current_profile, 
    chapter_id,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):
    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id, by_link=True)

    chapter_context = chapter_service.user_get_chapter_context(chapter, caller=current_profile)

    return respond(
        data=GetChapterSchemaFull().dump(chapter), 
        context=GetChapterContextSchema().dump(chapter_context)
    )