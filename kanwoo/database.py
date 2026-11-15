from sqlalchemy.orm.session import Session
from contextvars import ContextVar

nesting_level_var: ContextVar[int] = ContextVar('nesting_level', default=0)

class DBTransaction:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self._tokens = []

    def flush(self):
        self.db_session.flush()

    def __enter__(self):
        nesting_level = nesting_level_var.get()
        token = nesting_level_var.set(nesting_level + 1)
        self._tokens.append(token)
        return self

    def __exit__(self, exc_type, exc, tb):
        if not self._tokens:
            raise RuntimeError("Failed to get context token")
        
        token = self._tokens.pop()
        nesting_level_var.reset(token)

        if exc:
            self.db_session.rollback()
            return False

        if nesting_level_var.get() == 0:
            try:
                self.db_session.commit()
            except Exception:
                self.db_session.rollback()
                raise