from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from .schemas import (
    CollectionSchema, 
)
from .services import CollectionService, CollectionScope


from .handlers import (
    update_collection_handler,
    create_collection_handler,
    delete_collection_handler,
    add_manga_into_collection_handler,
    remove_manga_from_collection_handler,
    get_collection_manga_handler
)

bp = Blueprint('collections', __name__, url_prefix='/collections')

bp.add_url_rule("", view_func=create_collection_handler, strict_slashes=False, methods=["POST"])
bp.add_url_rule("/<int:collection_id>", view_func=update_collection_handler, methods=["PUT"])
bp.add_url_rule("/<int:collection_id>", view_func=delete_collection_handler, methods=["DELETE"])
bp.add_url_rule("/<int:collection_id>/manga", view_func=add_manga_into_collection_handler, methods=["PATCH"])
bp.add_url_rule("/<int:collection_id>/manga", view_func=remove_manga_from_collection_handler, methods=["DELETE"])
bp.add_url_rule("/<int:collection_id>/manga", view_func=get_collection_manga_handler, methods=["GET"])


@bp.route('', methods=['GET'], strict_slashes=False)
@profile_required()
@inject
def get_collections_route(
    current_profile,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collections = collection_service.user_get_profile_collections(current_profile, current_profile, scope=CollectionScope.CREATOR)

    return respond(data=CollectionSchema().dump(collections, many=True))

@bp.route('/<int:collection_id>', methods=['GET'])
@profile_required(optional=True)
@inject
def get_collection_route(
    current_profile, 
    collection_id,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collection = collection_service.user_get_collection_by_id(current_profile, collection_id)

    return respond(data=CollectionSchema().dump(collection))

@bp.route('/<int:collection_id>/save', methods=['POST'])
@profile_required()
@inject
def create_save_route(
    current_profile,    
    collection_id,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collection = collection_service.user_get_collection_by_id(current_profile, collection_id)

    collection_service.user_save_collection(current_profile, collection)

    return respond(data={"success": True})

@bp.route('/<int:collection_id>/save', methods=['DELETE'])
@profile_required()
@inject
def delete_save_route(
    current_profile,
    collection_id,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collection = collection_service.user_get_collection_by_id(current_profile, collection_id)

    collection_service.user_remove_save(current_profile, collection)

    return respond(data={"success": True})
