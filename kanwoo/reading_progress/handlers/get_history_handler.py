from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.middleware import pagination
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.reading_progress.schemas import GetReadingProgressSchema, GetReadingProgressContextSchema

@profile_required()
@pagination
@inject
def get_history_handler(
    current_profile,
    rp_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service],
    cursor = None
):
    progresses, cursor, has_more = rp_service.user_get_history(current_profile, cursor)

    progresses_contexts = [
        rp_service.user_get_progress_context(current_profile, p, include_manga=True, include_chapter=True) for p in progresses
    ]

    progress_schema = GetReadingProgressSchema()
    progress_context_schema = GetReadingProgressContextSchema()

    return respond(
        data=progress_schema.dump(progresses, many=True),
        context=progress_context_schema.dump(progresses_contexts, many=True),
        has_more=has_more,
        cursor=cursor
    )

