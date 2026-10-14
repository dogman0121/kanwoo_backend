from dependency_injector.wiring import inject, Provide
from flask import request

from kanwoo import AppContainer
from kanwoo.exceptions import ApiBadRequest
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.profile.services import ProfileService
from kanwoo.manga.services import MangaService
from kanwoo.studio.schemas import GetStudioProfileSchema, GetStudioProfilePermissionSchema


@profile_required()
@inject
def get_profile_handler(
    current_profile,
    profile_slug,
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    profile_permission = profile_service.user_get_profile_permission(current_profile, profile)

    return respond(
        data=GetStudioProfileSchema().dump(profile),
        permission=GetStudioProfilePermissionSchema().dump(profile_permission)
    )