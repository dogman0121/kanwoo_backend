from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required
from kanwoo.chapter.dto import UpdateChapterDTO
from kanwoo.chapter.services import ChapterService
from kanwoo.translation.services import TranslationService
from kanwoo.studio.schemas import UpdateStudioChapterSchema, GetStudioChapterSchema

@profile_required()
@inject
def update_chapter_handler(
    current_profile, 
    chapter_id,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):  
    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id)

    update_data = UpdateStudioChapterSchema().load({
        "name": request.form.get("name"),
        "chapter": request.form.get("chapter"),
        "privacy": request.form.get("privacy"),
        "pages": request.files.getlist("pages"),
        "pages_order": request.form.get("pages_order")
    })

    update_dto = UpdateChapterDTO(
        name=update_data.get("name"),
        chapter=update_data.get("chapter"),
        privacy=update_data.get("privacy"),
        pages=update_data.get("pages"),
        pages_order=update_data.get("pages_order")
    )
    
    chapter = chapter_service.user_update_chapter(current_profile, chapter, update_dto)

    return respond(data=GetStudioChapterSchema().dump(chapter))