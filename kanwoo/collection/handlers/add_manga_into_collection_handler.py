from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from kanwoo.collection.schemas import (
    CollectionAddMangaSchema, 
)
from kanwoo.collection.services import CollectionService
from kanwoo.collection.dto import (
    CollectionAddMangaDTO, 
)

@profile_required()
@inject
def add_manga_into_collection_handler(
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