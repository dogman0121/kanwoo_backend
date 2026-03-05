from flask import Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.middleware import profile_required
from kanwoo.utils import respond

from .services import HomeService
from .schemas import HomeSchema


bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('', methods=['GET'], strict_slashes=False)
@profile_required(optional=True)
@inject
def get_home_route(
    current_profile,
    home_service: HomeService = Provide[AppContainer.home_container.home_service]
):
    hero_slider = home_service.user_get_hero_slider()
    newest_manga = home_service.user_get_newest_manga()
    ended_manga = home_service.user_get_ended_manga()
    random_manga = home_service.user_get_random_manga()

    return respond(data=HomeSchema().dump({
        "hero": hero_slider,
        "newest": newest_manga,
        "ended": ended_manga,
        "random": random_manga,
    }))