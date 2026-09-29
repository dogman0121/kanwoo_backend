from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.reading_progress.schemas import GetReadingProgressContextSchema, GetReadingProgressSchema

from kanwoo.profile.middleware import profile_required
from kanwoo.profile.services import ProfileService

@profile_required()
@inject
def get_profile_progress_handler(
    current_profile,
    profile_slug,
    reading_progress_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service],
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    progresses = reading_progress_service.user_get_profile_progress(current_profile, profile)

    contexts = [reading_progress_service.user_get_reading_progress_context(current_profile, p, include_manga=True, include_chapter=True) for p in progresses]

    progress_schema = GetReadingProgressSchema()
    progress_context_schema = GetReadingProgressContextSchema()

    return respond(
        data=progress_schema.dump(progresses, many=True),
        context=progress_context_schema.dump(contexts, many=True)
    )
