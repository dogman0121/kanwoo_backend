from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.schemas import GetMangaSchemaMini
from kanwoo.chapter.schemas import GetChapterSchemaMini
from kanwoo.home.services import HomeService
from kanwoo.home.entities import HomeBlockType
from kanwoo.home.schemas import GetHomeBlockSchema

@profile_required(optional=True)
@inject
def get_home_block_handler(
    current_profile,
    hash,
    home_service: HomeService = Provide[AppContainer.home_container.home_service]
):

    type_, data = home_service.user_get_block_by_hash(current_profile, hash)

    return respond(data=GetHomeBlockSchema().dump((type_, data)))