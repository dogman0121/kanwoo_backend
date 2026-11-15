from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.middleware import pagination
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingHistoryService
from kanwoo.reading_progress.schemas import GetReadingHistorySchema, GetReadingHistoryContextSchema

@profile_required()
@pagination
@inject
def get_history_list_handler(
    current_profile,
    rh_service: ReadingHistoryService = Provide[AppContainer.reading_progress_container.reading_history_service],
    cursor = None
):
    history_list, cursor, has_more = rh_service.user_get_history(current_profile, cursor)

    progresses_contexts = [
        rh_service.user_get_history_context(
            current_profile, 
            history_item, 
            include_manga=True, 
            include_chapter=True
        ) for history_item in history_list
    ]

    return respond(
        data=GetReadingHistorySchema().dump(history_list, many=True),
        context=GetReadingHistoryContextSchema().dump(progresses_contexts, many=True),
        has_more=has_more,
        cursor=cursor
    )

