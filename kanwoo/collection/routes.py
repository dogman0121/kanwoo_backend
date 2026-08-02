from flask_jwt_extended import jwt_required
from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import db
from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from .schemas import (
    CollectionCreateSchema, 
    CollectionSchema, 
    CollectionUpdateSchema, 
    CollectionAddMangaSchema, 
    CollectionRemoveMangaSchema
)
from .services import CollectionService, CollectionScope
from .dto import (
    CollectionCreateDTO, 
    CollectionUpdateDTO, 
    CollectionAddMangaDTO, 
    CollectionRemoveMangaDTO
)

bp = Blueprint('lists', __name__, url_prefix='/lists')

@bp.route('', methods=['GET'], strict_slashes=False)
@profile_required()
@inject
def get_collections_route(
    current_profile,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collections = collection_service.user_get_profile_collections(current_profile, current_profile, scope=CollectionScope.CREATOR)

    return respond(data=CollectionSchema().dump(collections, many=True))


@bp.route('', methods=['POST'], strict_slashes=False)
@profile_required()
@inject
def create_collectiont_route(
    current_profile,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    create_schema = CollectionCreateSchema().load(request.json)

    create_dto = CollectionCreateDTO(
        name=create_schema.get("name"),
        privacy_id=create_schema.get("privacy")
    )

    collection = collection_service.user_create_collection(current_profile, create_dto)

    return respond(data=CollectionSchema().dump(collection)), 201

@bp.route('/<int:collection_id>', methods=['PUT'])
@profile_required()
@inject
def update_collection_route(
    current_profile, 
    collection_id,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collection = collection_service.user_get_collection_by_id(collection_id)

    name = request.form.get("name")
    description = request.form.get("description")
    privacy = request.form.get("privacy")

    update_schema = CollectionUpdateSchema().load({
        "name": name,
        "description": description,
        "privacy": privacy
    })

    update_dto = CollectionUpdateDTO(
        name=update_schema.get("name"),
        description=update_schema.get("description"),
        privacy_id=update_schema.get("privacy")
    )

    updated_collection = collection_service.user_update_list(current_profile, collection, update_dto)

    return respond(data=CollectionSchema().dump(updated_collection))

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

@bp.route('/<int:collection_id>', methods=['DELETE'])
@profile_required()
@inject
def delete_collection_route(
    current_profile,
    collection_id,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collection = collection_service.user_get_collection_by_id(current_profile, collection_id)

    collection_service.user_delete_collection(collection)

    return respond(data={"success": True})

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

@bp.route('/<int:collection_id>/manga', methods=['PATCH'])
@profile_required()
@inject
def add_manga_route(
    current_profile,
    collection_id,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collection = collection_service.user_get_collection_by_id(current_profile, collection_id)

    add_manga_schema = CollectionAddMangaSchema().load({
        "manga": request.json.get("manga")
    })

    add_manga_dto = CollectionAddMangaDTO(
        manga_slug=add_manga_schema.get("manga")
    )

    collection_service.user_add_manga_to_collection(current_profile, collection, add_manga_dto)

    return respond(data={"success": True})




@bp.route('/<int:collection_id>/manga', methods=['DELETE'])
@profile_required()
@inject
def remove_manga_route(
    current_profile,
    collection_id,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collection = collection_service.user_get_collection_by_id(current_profile, collection_id)

    remove_manga_schema = CollectionRemoveMangaSchema().load({
        "manga": request.json.get("manga")
    })

    remove_manga_dto = CollectionRemoveMangaDTO(
        manga_slug=remove_manga_schema.get("manga")
    )

    collection_service.user_remove_manga_from_collection(current_profile, collection, remove_manga_dto)

    return respond(data={"success": True})