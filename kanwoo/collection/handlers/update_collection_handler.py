from flask_jwt_extended import jwt_required
from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import db
from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from kanwoo.collection.schemas import (
    CollectionSchema, 
    CollectionUpdateSchema, 
)
from kanwoo.collection.services import CollectionService
from kanwoo.collection.dto import (
    CollectionUpdateDTO, 
)

@profile_required()
@inject
def update_collection_handler(
    current_profile, 
    collection_id,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collection = collection_service.user_get_collection_by_id(current_profile, collection_id)

    update_schema = CollectionUpdateSchema().load(request.json)

    update_dto = CollectionUpdateDTO(
        name=update_schema.get("name"),
        description=update_schema.get("description"),
        privacy_id=update_schema.get("privacy")
    )

    updated_collection = collection_service.user_update_collection(current_profile, collection, update_dto)

    return respond(data=CollectionSchema().dump(updated_collection))