from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from .schemas import (
    GetCollectionSchema, 
)
from .services import CollectionService


from .handlers import (
    update_collection_handler,
    create_collection_handler,
    delete_collection_handler,
    add_manga_into_collection_handler,
    remove_manga_from_collection_handler,
    get_collection_manga_handler,
    get_collections_list_handler,
    save_collection_handler,
    unsave_collection_handler,
    get_collection_handler
)

bp = Blueprint('collections', __name__, url_prefix='/collections')

bp.add_url_rule("", view_func=get_collections_list_handler, strict_slashes=False, methods=["GET"])
bp.add_url_rule("", view_func=create_collection_handler, strict_slashes=False, methods=["POST"])
bp.add_url_rule("/<int:collection_id>", view_func=get_collection_handler, methods=["GET"])
bp.add_url_rule("/<int:collection_id>", view_func=update_collection_handler, methods=["PUT"])
bp.add_url_rule("/<int:collection_id>", view_func=delete_collection_handler, methods=["DELETE"])
bp.add_url_rule("/<int:collection_id>/manga", view_func=add_manga_into_collection_handler, methods=["PATCH"])
bp.add_url_rule("/<int:collection_id>/manga", view_func=remove_manga_from_collection_handler, methods=["DELETE"])
bp.add_url_rule("/<int:collection_id>/manga", view_func=get_collection_manga_handler, methods=["GET"])
bp.add_url_rule("/<int:collection_id>/saves", view_func=save_collection_handler, methods=["POST"])
bp.add_url_rule("/<int:collection_id>/saves", view_func=unsave_collection_handler, methods=["DELETE"])
