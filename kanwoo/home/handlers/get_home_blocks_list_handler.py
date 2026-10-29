from flask import request
from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.home.services import HomeService
from kanwoo.home.schemas import GetHomeBlockSchema, GetHomeBlocksListSchema

@profile_required(optional=True)
@inject
def get_home_blocks_list_handler(
    current_profile,
    home_service: HomeService = Provide[AppContainer.home_container.home_service]
):
    blocks_hash = GetHomeBlocksListSchema().load(request.json).get("blocks_hash")

    data = []
    for b_hash in blocks_hash:
        type_, block_data = home_service.user_get_block_by_hash(current_profile, b_hash)
        data.append((type_, block_data))

    return respond(data=GetHomeBlockSchema(many=True).dump(data))