from app.list.models import List

class ListRepository:
    @staticmethod
    def create_list(list: List):
        list.add(commit=True)

        return list
    
    @staticmethod
    def get_list(list_id: int):
        list = List.query.filter_by(id=list_id).first()

        return list