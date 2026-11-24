
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required
from kanwoo.collection.schemas import GetCollectionSchema
from kanwoo.collection.services import CollectionService
from kanwoo.collection.entities import CollectionScope

@profile_required()
@inject
def get_collections_list_handler(
    current_profile,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collections = collection_service.user_get_profile_collections(current_profile, current_profile, scope=CollectionScope.CREATOR)

    return respond(data=GetCollectionSchema().dump(collections, many=True))