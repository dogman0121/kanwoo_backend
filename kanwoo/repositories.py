from sqlalchemy.orm.session import Session
from sqlalchemy import select, insert

class BaseRepository:
    model = None

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id_):
        return self.db_session.execute(select(self.model).filter(self.model.id == id_)).scalar()

    def create(self, entity):
        self.db_session.add(entity)

    def update(self, entity, data: dict):
        for key, val in data.items():
            setattr(entity, key, val)

        self.db_session.add(entity)

    def delete(self, entity):
        self.db_session.delete(entity)