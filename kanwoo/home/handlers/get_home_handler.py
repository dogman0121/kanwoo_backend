from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.home.services import HomeService
from kanwoo.home.schemas import GetHomeMapItemSchema


@profile_required(optional=True)
@inject
def get_home_handler(
    current_profile,
    home_service: HomeService = Provide[AppContainer.home_container.home_service]
):

    home_map = home_service.user_get_home_map(current_profile)

    return respond(data=GetHomeMapItemSchema().dump(home_map, many=True))