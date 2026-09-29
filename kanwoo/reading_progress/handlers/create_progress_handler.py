from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.chapter.services import ChapterService
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.reading_progress.schemas import CreateReadingProgressSchema
from kanwoo.reading_progress.dto import CreateReadingProgressDTO

@profile_required()
@inject
def create_progress_handler(
    current_profile,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service], 
    rp_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service]
):

    create_schema = CreateReadingProgressSchema().load(request.json)

    chapter_id=create_schema.get("chapter_id")

    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id)

    create_dto = CreateReadingProgressDTO(
        chapter=chapter,
        page=create_schema.get("page")
    )

    progress = rp_service.user_create_progress(current_profile, create_dto)

    return respond(data={"id": progress.id})