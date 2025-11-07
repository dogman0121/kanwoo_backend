from app.exceptions import ApiNotFound
from app.utils import respond

from . import bp

from .exceptions import ChapterNotFoundException
from .services import ChapterService
from .schemas import ChapterSchemaFull

@bp.route("/<int:chapter_id>", methods=["GET"])
def get_chapter_route(chapter_id):
    try:
        chapter = ChapterService.get_chapter_by_id(chapter_id)

        schema = ChapterSchemaFull()

        return respond(data=schema.dump(chapter))
    except ChapterNotFoundException:
        raise ApiNotFound


@bp.route("/<int:chapter_id>/info", methods=["GET"])
def get_info_form_route(chapter_id):
    pass


@bp.route("/<int:chapter_id>/info", methods=["PUT"])
def update_chapter_info_route(chapter_id):
    pass
