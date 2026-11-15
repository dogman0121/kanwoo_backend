from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer, respond
from kanwoo.frontend_metadata import FrontendMetadataSchema
from kanwoo.profile.middleware import profile_required
from kanwoo.chapter.services import ChapterFrontendMetadataService


@profile_required(optional=True)
@inject
def get_chapter_metadata_handler(
    current_profile,
    chapter_id,
    frontend_metadata_service: ChapterFrontendMetadataService = Provide[AppContainer.chapter_container.chapter_frontend_metadata_service]
):
    metadata = frontend_metadata_service.get(chapter_id)

    return respond(data=FrontendMetadataSchema().dump(metadata))
    