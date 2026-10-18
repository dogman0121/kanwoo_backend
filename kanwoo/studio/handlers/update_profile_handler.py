from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required
from kanwoo.profile.services import ProfileService
from kanwoo.profile.dto import UpdateProfileDTO
from kanwoo.profile.schemas import AvatarAction
from kanwoo.studio.schemas import UpdateStudioProfileSchema, GetStudioProfileSchema

@profile_required()
@inject
def update_profile_handler(
    current_profile, 
    profile_slug,
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service]
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    update_data = UpdateStudioProfileSchema().load({
        "name": request.form.get("name"),
        "slug": request.form.get("slug"),
        "avatar_action": request.form.get("avatar_action"),
        "about": request.form.get("about", ""),
        "links": request.form.get("links"),
        "avatar": request.files.get("avatar"),
    })

    profile_update_dto = UpdateProfileDTO(
        name = update_data.get("name"),
        slug = update_data.get("slug"),
        about = update_data.get("about"),
        links = update_data.get("links"),
        avatar_action = update_data.get("avatar_action", AvatarAction.KEEP),
        avatar = update_data.get("avatar")
    )

    profile = profile_service.user_update_profile(current_profile, profile, profile_update_dto)    

    return respond(data=GetStudioProfileSchema().dump(profile))