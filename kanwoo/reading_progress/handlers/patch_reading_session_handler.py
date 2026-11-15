from flask import request
from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.chapter.services import ChapterService
from kanwoo.database import DBTransaction
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingBookmarkService, ReadingSessionService
from kanwoo.reading_progress.schemas import UpdateReadingSessionSchema
from kanwoo.reading_progress.dto import UpdateReadingSessionDTO

@profile_required()
@inject
def patch_reading_session_handler(
    current_profile,
    session_id,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
    bookmark_service: ReadingBookmarkService = Provide[AppContainer.reading_progress_container.reading_bookmark_service],
    session_service: ReadingSessionService = Provide[AppContainer.reading_progress_container.reading_session_service],
    db_transaction: DBTransaction = Provide[AppContainer.db_transaction]
):
    update_data = UpdateReadingSessionSchema().load(request.json)

    with db_transaction:
        session = session_service.user_get_reading_session_by_id(current_profile, session_id)

        page = update_data.get("page")
        chapter_id = update_data.get("chapter_id")
        is_finished = update_data.get('is_finished')

        chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id, by_link=True)

        update_dto = UpdateReadingSessionDTO(
            chapter_id=chapter_id,
            page=page,
            is_finished=is_finished
        )

        session_service.update_reading_session(
            current_profile,
            session,
            update_dto
        )

        # Обновляем закладку
        manga = session.translation.manga
        translation = session.translation
        bookmark_chapter_number = chapter.chapter
        bookmark_page_number = page

        # Если пользователь закончил читать главу, меняет закладку на следующую
        if is_finished:
            bookmark_chapter_number += 1
            bookmark_page_number = 0

        bookmark_service.set_reading_bookmark(
            current_profile,
            manga,
            translation,
            bookmark_chapter_number,
            bookmark_page_number,
        )

    return respond(data={"success": True})