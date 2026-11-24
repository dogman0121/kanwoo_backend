from flask import request, Response
from dependency_injector.wiring import Provide, inject
from functools import wraps
from enum import Enum
from sqlalchemy import text, insert, select, update
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy.dialects.postgresql import insert as psql_insert

from kanwoo import AppContainer
from kanwoo.auth.services import HashService
from kanwoo.unit_of_work import transaction_status, TransactionStatusEnum
from kanwoo.unit_of_work import UnitOfWork
from kanwoo.idempotency.models import Idempotency

from .exceptions import IdempotencyError

class AcquiredResponseEnum(Enum):
    ACQUIRED = 0
    TIMEOUT = 1
    EXISTS = 2

def acquire(db_session, key):

    try:
        db_session.execute(text("SET LOCAL lock_timeout = '100ms'"))

        result = db_session.execute(
            psql_insert(
                Idempotency
            ).values(
                uuid=key
            )
            .on_conflict_do_nothing(
                index_elements=[Idempotency.uuid]
            )
            .returning(Idempotency.uuid)
        )
    except OperationalError as exc:
        if getattr(exc.orig, "sqlstate", None) == "55P03":
            return AcquiredResponseEnum.TIMEOUT
    finally:
        db_session.execute(text("SET LOCAL lock_timeout = DEFAULT"))

    if result is None:
        return AcquiredResponseEnum.EXISTS
    return AcquiredResponseEnum.ACQUIRED


def idemponent(func):
    @wraps(func)
    @inject
    def wrapper(
        *args, 
        uow: UnitOfWork = Provide[AppContainer.unit_of_work],
        hash_service: HashService = Provide[AppContainer.auth_container.hash_service],
        **kwargs,
    ):

        idempotency_key = request.headers.get("Idempotency-Key")

        if idempotency_key is None:
            raise IdempotencyError(
                error="idempotency_key_required",
                detail={
                    "Idempotency-Key": ["Idempotency key is required."]
                },
                status_code=400
            )

        request_hash = hash_service.generate_hash(
            (request.path + "::" + request.method + "::" + request.get_data(as_text=True)).encode()
        )

        with uow:
            locked_status = acquire(uow.db_session, idempotency_key)

            if locked_status == AcquiredResponseEnum.EXISTS:
                idempotency_sql_model = uow.db_session.execute(
                    select(Idempotency).where(Idempotency.uuid==idempotency_key)
                ).scalar_one_or_none()

                if idempotency_sql_model.request_hash != request_hash:
                    raise IdempotencyError(
                        error="request_does_not_match",
                        status_code=409
                    )

                if idempotency_sql_model:                
                    return Response(
                        response=Idempotency.body, 
                        status=Idempotency.status_code,
                        mimetype="application/json"
                    )
            elif locked_status == AcquiredResponseEnum.TIMEOUT:
                raise IdempotencyError(
                    error="operation_in_progress",
                    detail={
                        "Idempotency-Key": ["Operation with this Idempotency-Key in progress."]
                    },
                    status_code=409
                )

            response: Response = func(*args, **kwargs)
            
            if (response.status_code // 100 == 2 or \
                (response.status_code // 100 == 5  and transaction_status.get() != TransactionStatusEnum.ROLLED_BACK)
            ):
                uow.db_session.execute(update(Idempotency).values(
                    status_code=response.status_code,
                    request_hash=request_hash,
                    body=response.get_data(as_text=True)
                ).where(
                    Idempotency.uuid == idempotency_key
                ))

            return response

    return wrapper