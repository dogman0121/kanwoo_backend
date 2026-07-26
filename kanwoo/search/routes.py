from flask import jsonify, request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.middleware import pagination
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
@pagination
@inject
def search_route(
    current_profile,
    search_service: SearchService = Provide[AppContainer.search_container.search_service],
    page=1,
    per_page=20
):
    query = request.args.get('query', type=str)
    section = request.args.get('section', 'manga', type=str)

    if section == "manga":
        types = request.args.getlist("type", type=int)
        genres = request.args.getlist("genre", type=int)
        statuses = request.args.getlist("status", type=int)
        adults = request.args.getlist("adult", type=int)
        year_from = request.args.get("year_from", type=int)
        year_to = request.args.get("year_to", type=int)

        search_dto = SearchMangaDTO(
            query=query,
            genres=genres if genres != [] else None,
            types=types if types != [] else None,
            adults=adults if adults != [] else None,
            statuses=statuses if statuses != [] else None,
            year_from=year_from,
            year_to=year_to
        )

        search_results, total_count = search_service.user_search_manga(current_profile, search_dto, page, per_page)

        results = MangaSchema().dump(search_results, many=True) 
    if section == "user":
        total_count = 0
        results = []

    return respond(
        data=results,
        page=page,
        per_page=per_page,
        total_count=total_count
    )