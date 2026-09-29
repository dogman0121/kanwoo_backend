from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.schemas import GetMangaSchemaMini
from kanwoo.chapter.schemas import GetChapterSchemaMini
from kanwoo.home.services import HomeService
from kanwoo.home.entities import HomeBlockType
from kanwoo.home.schemas import GetHeroBlockSchema, GetHomeReadingProgressSchema

@profile_required(optional=True)
@inject
def get_home_block_handler(
    current_profile,
    hash,
    home_service: HomeService = Provide[AppContainer.home_container.home_service]
):

    type_, data = home_service.user_get_block_by_hash(current_profile, hash)

    if type_ == HomeBlockType.HERO:
        return respond(data=GetHeroBlockSchema().dump(data, many=True))
    elif type_ == HomeBlockType.MANGA_LIST:
        return respond(data=GetMangaSchemaMini().dump(data, many=True))
    elif type_ == HomeBlockType.LAST_ADDED_CHAPTERS:
        return respond(data=GetChapterSchemaMini().dump(data, many=True))
    else:
        raise ValueError("Failed to interpretate block type")