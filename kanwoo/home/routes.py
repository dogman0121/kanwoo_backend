from flask import Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.profile.middleware import profile_required
from kanwoo.utils import respond
from kanwoo.manga.schemas import MangaSchema

from .services import HomeService
from .schemas import HeroBlockSchema


bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/hero', methods=['GET'], strict_slashes=False)
@profile_required(optional=True)
@inject
def get_hero_slides_route(
    current_profile,
    home_service: HomeService = Provide[AppContainer.home_container.home_service]
):
    hero_slides = home_service.user_get_hero_slides(current_profile)

    return respond(data=HeroBlockSchema().dump(hero_slides, many=True))

@bp.route('/ended', methods=['GET'], strict_slashes=False)
@profile_required(optional=True)
@inject
def get_ended_manga_route(
    current_profile,
    home_service: HomeService = Provide[AppContainer.home_container.home_service]
):
    ended_manga = home_service.user_get_ended_manga(current_profile)

    return respond(data=MangaSchema().dump(ended_manga, many=True))

@bp.route('/newest', methods=['GET'], strict_slashes=False)
@profile_required(optional=True)
@inject
def get_newest_manga_route(
    current_profile,
    home_service: HomeService = Provide[AppContainer.home_container.home_service]
):
    newest_manga = home_service.user_get_newest_manga(current_profile)

    return respond(data=MangaSchema().dump(newest_manga, many=True))

@bp.route('/most-viewed', methods=['GET'], strict_slashes=False)
@profile_required(optional=True)
@inject
def get_most_viewed_route(
    current_profile,
    home_service: HomeService = Provide[AppContainer.home_container.home_service]
):
    most_viewed_manga = home_service.user_get_most_viewed_manga(current_profile)

    return respond(data=MangaSchema().dump(most_viewed_manga, many=True))