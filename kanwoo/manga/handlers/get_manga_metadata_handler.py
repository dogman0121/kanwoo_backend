from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer, respond
from kanwoo.frontend_metadata import FrontendMetadataSchema
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaFrontendMetadataService


@profile_required(optional=True)
@inject
def get_manga_metadata_handler(
    current_profile,
    manga_slug,
    frontend_metadata_service: MangaFrontendMetadataService = Provide[AppContainer.manga_container.manga_frontend_metadata_service]
):
    metadata = frontend_metadata_service.get(manga_slug)

    return respond(data=FrontendMetadataSchema().dump(metadata))
    