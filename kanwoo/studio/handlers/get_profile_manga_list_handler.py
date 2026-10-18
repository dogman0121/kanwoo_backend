from dependency_injector.wiring import inject, Provide
from flask import request

from kanwoo import AppContainer
from kanwoo.exceptions import ApiBadRequest
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.profile.services import ProfileService
from kanwoo.manga.services import MangaService
from kanwoo.studio.schemas import GetStudioMangaSchema


@profile_required()
@inject
def get_profile_manga_list_handler(
    current_profile,
    profile_slug,
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    manga_list = manga_service.user_get_profile_manga(current_profile, profile)

    return respond(
        data=GetStudioMangaSchema(many=True).dump(manga_list)
    )