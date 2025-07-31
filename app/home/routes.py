from . import bp
from .services import HomeService
from ..manga.models import Manga
from ..utils import respond


@bp.route('', methods=['GET'], strict_slashes=False)
def get_home():
    return respond(data={
        "slider": [m.to_dict() for m in Manga.get_most_viewed()],
        "newest": [m.to_dict() for m in Manga.get_newest()],
        "ended": [m.to_dict() for m in Manga.get_ended()],
        "random": [m.to_dict() for m in Manga.get_random()],
    })