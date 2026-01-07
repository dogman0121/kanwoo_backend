from app.list.models import ListManga, List, ListVisibility
from app.list.repositories import ListRepository
from app.list.exceptions import ListNotFound


class ListService:
    def __init__(self, user):
        self.user = user

    def create_list(self, name: str, description: str, visibility: ListVisibility):
        list = List(
            name=name,
            description=description,
            visibility=visibility,
            creator=self.user
        )

        return ListRepository.create_list(list)

    def get_list(self, list_id):
        list = ListRepository.get_list(list_id)

        if list is None:
            raise ListNotFound
        
        return list

    @staticmethod
    def get_user_lists_with_manga(manga, user):
        return List.query.join(ListManga, ListManga.list_id == List.id).filter(
            ListManga.manga_id == manga.id,
            List.creator_id == user.id
        ).all()