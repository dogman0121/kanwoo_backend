from sqlalchemy.orm.session import Session


class DBTransaction:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def flush(self):
        self.db_session.flush()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc, tb):
        if exc:
            self.db_session.rollback()
            raise exc

        self.db_session.commit()