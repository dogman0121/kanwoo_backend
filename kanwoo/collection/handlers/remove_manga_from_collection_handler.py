from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from kanwoo.collection.schemas import (
    RemoveMangaFromCollectionSchema
)
from kanwoo.collection.services import CollectionService
from kanwoo.collection.dto import ( 
    CollectionRemoveMangaDTO
)


@profile_required()
@inject
def remove_manga_from_collection_handler(
    current_profile,
    collection_id,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collection = collection_service.user_get_collection_by_id(current_profile, collection_id)

    remove_manga_schema = RemoveMangaFromCollectionSchema().load(request.json)

    remove_manga_dto = CollectionRemoveMangaDTO(
        manga_id=remove_manga_schema.get("manga_id")
    )

    collection_service.user_remove_manga_from_collection(current_profile, collection, remove_manga_dto)

    return respond(data={"success": True})