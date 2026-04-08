from flask import jsonify, request, Blueprint
from dependency_injector.wiring import inject, Provide


from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.schemas import MangaSchema
from kanwoo.exceptions import ApiNotFound

from .services import SearchService
from .dto import SearchMangaDTO


bp = Blueprint('search', __name__)

def parse_manga_filters():
    types = request.args.getlist("type", type=int)
    genres = request.args.getlist("genre", type=int)
    statuses = request.args.getlist("status", type=int)
    adult = request.args.getlist("adult", type=int)


    return {
        "types": types,
        "genres": genres,
        "statuses": statuses,
        "adult": adult
    }

@bp.route('', methods=['GET'], strict_slashes=False)
@profile_required(optional=True)
@inject
def search_route(
    current_profile,
    search_service: SearchService = Provide[AppContainer.search_container.search_service]
):
    query = request.args.get('query', type=str)
    section = request.args.get('section')

    if section == "manga":
        types = request.args.getlist("type", type=int)
        genres = request.args.getlist("genre", type=int)
        statuses = request.args.getlist("status", type=int)
        adults = request.args.getlist("adult", type=int)
        year_from = request.args.get("year_from", type=int)
        year_to = request.args.get("year_to", type=int)

        search_dto = SearchMangaDTO(
            query=query,
            genres=genres if len(genres) else None,
            types=types if len(types) else None,
            adults=adults if len(adults) else None,
            statuses=statuses if len(statuses) else None,
            year_from=year_from,
            year_to=year_to
        )

        search_result = search_service.user_search_manga(current_profile, search_dto)

        return respond(data=MangaSchema().dump(search_result, many=True))

    if section == "user":
        pass

    raise ApiNotFound