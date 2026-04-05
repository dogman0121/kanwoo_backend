from unittest.mock import create_autospec

from kanwoo import AppContainer
from kanwoo import db
from kanwoo.collection.repositories import CollectionRepository
from kanwoo.collection.dto import CollectionCreateDTO
from kanwoo.profile.models import Profile


def test_create_collection(app, container, profile_id):
    with app.app_context():
        profile = db.session.get(Profile, profile_id)
        
    collection_name = "test_create_collection"
    privacy_id = 0

    collection_create_dto = CollectionCreateDTO(
        name=collection_name,
        privacy_id=privacy_id
    )

    mock_collection_repo  = create_autospec(CollectionRepository)

    with (
        container.collection_container.collection_repo.override(mock_collection_repo),
    ):
        collection_service = container.collection_container.collection_service()

        with app.app_context():
            collection = collection_service.user_create_collection(profile, collection_create_dto)

    assert collection.name == collection_name
    assert collection.privacy_id == collection.privacy_id

    mock_collection_repo.create_collection.assert_called()
