from . import bp
from .services import HomeService
from .schemas import HomeSchema
from ..manga.models import Manga
from ..utils import respond

from app.profiles.middleware import profile_required


@bp.route('', methods=['GET'], strict_slashes=False)
@profile_required(optional=True)
def get_home(profile):
    schema = HomeSchema()

    home_service = HomeService(profile)

    hero_slider = home_service.get_featured_manga()
    newest_manga = home_service.get_newest_manga()
    ended_manga = home_service.get_ended_manga()
    random_manga = home_service.get_random_manga()

    return respond(data=schema.dump({
        "hero": hero_slider,
        "newest": newest_manga,
        "ended": ended_manga,
        "random": random_manga,
    }))