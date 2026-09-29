from dependency_injector.wiring import inject, Provide

from kanwoo import db
from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from kanwoo.collection.services import CollectionService

@profile_required()
@inject
def delete_collection_handler(
    current_profile,
    collection_id,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service]
):
    collection = collection_service.user_get_collection_by_id(current_profile, collection_id)

    collection_service.user_delete_collection(current_profile, collection)

    return respond(data={"success": True})