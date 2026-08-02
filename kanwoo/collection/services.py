from enum import Enum

from kanwoo.database import DBTransaction
from kanwoo.manga.repositories import MangaRepository

from .models import Collection
from .repositories import CollectionRepository
from .exceptions import CollectionNotFoundException, CollectionUpdateNotAllowedException, CollectionDeleteNotAllowedException
from .dto import CollectionCreateDTO, CollectionUpdateDTO, CollectionAddMangaDTO, CollectionRemoveMangaDTO
from .permissions import CollectionPolicy

class CollectionScope(Enum):
    CREATOR = "creator"
    ALL = "all"

class CollectionService:

    def __init__(
        self, 
        collection_repo: CollectionRepository,
        db_transaction: DBTransaction,
        collection_policy: CollectionPolicy,
        manga_repo: MangaRepository
    ):
        self.collection_repo = collection_repo
        self.db_transaction = db_transaction
        self.collection_policy = collection_policy
        self.manga_repo = manga_repo

    def user_get_collections(self, profile):
        collections = self.collection_repo.get_profile_collections(profile.id)

        return collections

    def user_get_profile_collections(
            self, 
            current_profile, 
            profile,
            scope=CollectionScope.ALL,
        ):
            if scope == CollectionScope.ALL:
                return self.collection_repo.get_profile_collections(current_profile.id, profile.id)
            elif CollectionScope.CREATOR:
                return self.collection_repo.get_profile_owned_collections(current_profile.id, profile.id)

    def user_get_collection_by_id(self, profile, collection_id: int):
        collection = self.collection_repo.get_collection_by_id_from_user(profile.id, collection_id)

        if collection is None:
            raise CollectionNotFoundException()

        return collection

    def user_create_collection(self, profile, data: CollectionCreateDTO):
        collection = Collection(
            name=data.name,
            creator_id=profile.id,
            privacy_id=data.privacy_id
        )

        with self.db_transaction:
            self.collection_repo.create_collection(collection)

        return collection

    def user_update_collection(self, profile, collection, data: CollectionUpdateDTO):
        if not self.collection_policy.can_update(profile, collection):
            raise CollectionUpdateNotAllowedException()
        
        collection.name = data.name
        collection.description = data.description
        collection.privacy_id = data.privacy_id
        
        with self.db_transaction:
            self.collection_repo.update_collection(collection)

        return collection

    def user_delete_collection(self, profile, collection):
        if not self.collection_policy.can_delete(profile, collection):
            raise CollectionDeleteNotAllowedException()

        with self.db_transaction:
            self.collection_repo.delete_collection(collection)

    def user_add_manga_to_collection(self, profile, collection, data: CollectionAddMangaDTO):
        if not self.collection_policy.can_update(profile, collection):
            raise CollectionUpdateNotAllowedException()
        
        with self.db_transaction:
            manga = self.manga_repo.get_manga_by_slug_from_user(profile, data.manga_slug)
            
            self.collection_repo.add_manga_to_collection(collection, manga.id)

    def user_remove_manga_from_collection(self, profile, collection, data: CollectionRemoveMangaDTO):
        if not self.collection_policy.can_update(profile, collection):
            raise CollectionUpdateNotAllowedException()

        with self.db_transaction:
            manga = self.manga_repo.get_manga_by_slug_from_user(profile.id, data.manga_slug)

            self.collection_repo.remove_manga_from_collection(collection, manga.id)

    def user_save_collection(self, profile, collection):
        
        with self.db_transaction:
            self.collection_repo.save_collection(profile.id, collection.id)


    def user_unsave_collection(self, profile, collection):
        
        with self.db_transaction:
            self.collection_repo.unsave_collection(profile.id, collection.id)