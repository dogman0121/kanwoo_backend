from flask_jwt_extended import jwt_required
from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import db
from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from kanwoo.collection.schemas import (
    CollectionCreateSchema, 
    CollectionSchema, 
)
from kanwoo.collection.services import CollectionService
from kanwoo.collection.dto import (
    CollectionCreateDTO,  
)

@profile_required()
@inject
def create_collection_handler(
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