from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.exceptions import ApiBadRequest
from kanwoo.utils import respond
from kanwoo.profile.services import ProfileService
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaService
from kanwoo.manga.schemas import GetMangaSchemaFull
from kanwoo.manga.dto import CreateMangaDTO


@profile_required(optional=True)
@inject
def get_manga_list_handler(
    current_profile, 
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    if "profile_id" in request.args:
        profile = profile_service.user_get_profile_by_slug(current_profile, request.args.get("profile_id"))

        manga_list = manga_service.user_get_profile_manga(current_profile, profile)
    else:
        raise ApiBadRequest()

    return respond(
        data=GetMangaSchemaFull().dump(manga_list, many=True)
    )
