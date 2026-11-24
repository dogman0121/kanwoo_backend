from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone, timedelta

from kanwoo.models import BaseModel


class Idempotency(BaseModel):
    __tablename__ = "idempotency"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    request_hash: Mapped[str] = mapped_column(nullable=True)
    status_code: Mapped[int] = mapped_column(nullable=True)
    body: Mapped[str] = mapped_column(nullable=True)
    expires_at: Mapped[str] = mapped_column(default=lambda: datetime.now(timezone.utc) + timedelta(minutes=30))