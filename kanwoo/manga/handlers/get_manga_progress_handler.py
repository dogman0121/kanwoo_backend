from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.reading_progress.schemas import GetReadingProgressContextSchema, GetReadingProgressSchema
from kanwoo.manga.services import MangaService


@profile_required()
def get_manga_progress_handler(
    current_profile, 
    manga_slug,
    reading_progress_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    progress = reading_progress_service.user_get_manga_progress(current_profile, manga)

    progress_schema = GetReadingProgressSchema()
    progress_context_schema = GetReadingProgressContextSchema()

    return respond(
        data=progress_schema.dump(progress), 
        context=progress_context_schema().dump(
            reading_progress_service.user_get_reading_progress_context(current_profile, progress, include_chapter=True)
        )
    )