from app.exceptions import ApiNotFound
from app.utils import respond

from . import bp

from .exceptions import TranslationNotFoundException
from .services import TranslationService
from .schemas import TranslationSchemaFull


@bp.route("/<int:translation_id>", methods=["GET"])
def get_translation_route(translation_id):
    try:
        translation = TranslationService.get_translation_by_id(translation_id)

        schema = TranslationSchemaFull()

        return respond(data=schema.dump(translation))
    except TranslationNotFoundException:
        raise ApiNotFound


@bp.route("/<int:chapter_id>/info", methods=["GET"])
def get_translation_form_route(chapter_id):
    pass


@bp.route("/<int:chapter_id>/info", methods=["PUT"])
def update_translation_info_route(chapter_id):
    pass

@bp.route("/<int:translation_id>/chapters", methods=["POST"])
def create_translation_chapter():
    pass
