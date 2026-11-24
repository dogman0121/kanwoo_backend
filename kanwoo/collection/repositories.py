from sqlalchemy import select, delete, update, exists
from sqlalchemy.orm import selectinload

from kanwoo.repositories import BaseRepository
from kanwoo.collection.models import Collection, CollectionManga, CollectionSave

class CollectionRepository(BaseRepository):

    def get_collection_by_id_from_user(self, profile_id, collection_id):
        return self.db_session.execute(
            select(Collection).filter(
                Collection.id==collection_id, 
                Collection.can_view(profile_id) == True
            )
        ).scalar()
    
    def get_profile_owned_collections(self, viewer_id, profile_id):
        
        return self.db_session.execute(
            select(Collection).filter(
                Collection.creator_id==profile_id,
                Collection.can_view(viewer_id)==True
            ).options(selectinload(Collection.manga))
        ).scalars().all()

    def get_profile_collections(self, viewer_id, profile_id):
        return self.db_session.execute(
            select(Collection).select_from(
                select(Collection).filter(
                    Collection.creator_id==profile_id, 
                    Collection.can_view(profile_id)==True
                ).union(
                    select(Collection).join(CollectionSave, Collection.id == CollectionSave.collection_id)
                    .filter(
                        CollectionSave.profile_id==profile_id,
                        Collection.can_view(viewer_id)==True
                    )
                )
            ).options(selectinload(Collection.manga))
        ).scalars().all()

    def create_collection(self, collection):
        self.db_session.add(collection)

        return collection

    def update_collection(self, collection):
        self.db_session.merge(collection)

        return collection

    def delete_collection(self, collection):
        self.db_session.delete(collection)

    def add_manga_to_collection(self, collection, manga_id):
        
        self.db_session.add(
            CollectionManga(
                collection_id=collection.id,
                manga_id=manga_id
            )
        )

    def remove_manga_from_collection(self, collection, manga_id):
        
        self.db_session.execute(
            delete(CollectionManga)
            .filter(
                CollectionManga.collection_id==collection.id,
                CollectionManga.manga_id==manga_id
            )
        )

    def save_collection(self, profile_id, collection_id, commit=True):
        
        self.db_session.add(
            CollectionSave(
                profile_id=profile_id,
                collection_id=collection_id
            )
        )

    def unsave_collection(self, profile_id, collection_id):
        
        self.db_session.execute(
            delete(CollectionSave)
            .filter(
                CollectionSave.profile_id==profile_id,
                CollectionSave.collection_id==collection_id
            )
        )

    def get_collections_with_manga(self, actor_id, manga_id):
        return self.db_session.execute(
            select(Collection)
            .join(CollectionManga, Collection.id == CollectionManga.collection_id)
            .filter
            (
                Collection.creator_id == actor_id, 
                CollectionManga.manga_id == manga_id
            )
        ).scalars().all()

    def check_collection_has_manga(self, collection_id: int, manga_id: int):
        return self.db_session.execute(
            select(
                select(Collection)
                .join(CollectionManga, Collection.id == CollectionManga.collection_id)
                .filter
                (
                    Collection.id == collection_id, 
                    CollectionManga.manga_id == manga_id
                ).exists()
            )
        ).scalar()

    def check_collection_is_subscribed_by_user(self, profile_id, collection_id):
        return self.db_session.execute(
            select(
                select(Collection)
                .join(CollectionSave, Collection.id == CollectionSave.collection_id)
                .filter
                (
                    Collection.id == collection_id, 
                    CollectionSave.profile_id == profile_id
                ).exists()
            )
        ).scalar()