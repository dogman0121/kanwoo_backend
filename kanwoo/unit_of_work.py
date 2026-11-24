from sqlalchemy.orm.session import Session
from contextvars import ContextVar
from enum import Enum

class TransactionStatusEnum(Enum):
    OPENED = "opened"
    CLOSED = "closed"
    ROLLED_BACK = "rolled_back"
    UNKNOWN = "unknown"

nesting_level_var: ContextVar[int] = ContextVar('nesting_level', default=0)

transaction_status: ContextVar[TransactionStatusEnum] = ContextVar(
    'transaction_status', 
    default=TransactionStatusEnum.UNKNOWN
)


class UnitOfWork:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self._tokens = []

    def flush(self):
        self.db_session.flush()

    def __enter__(self):
        nesting_level = nesting_level_var.get()
        token = nesting_level_var.set(nesting_level + 1)
        self._tokens.append(token)
        transaction_status.set(TransactionStatusEnum.OPENED)
        return self

    def __exit__(self, exc_type, exc, tb):
        if not self._tokens:
            raise RuntimeError("Failed to get context token")
        
        token = self._tokens.pop()
        nesting_level_var.reset(token)

        if nesting_level_var.get() == 0:
            try:
                self.db_session.commit()
                transaction_status.set(TransactionStatusEnum.CLOSED)
            except Exception:
                self.db_session.rollback()
                transaction_status.set(TransactionStatusEnum.ROLLED_BACK)
                raise

        return False