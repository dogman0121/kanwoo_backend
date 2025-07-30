from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.infrastructure.models.sql_file import SQLFile


class SQLMangaPosterFile(SQLFile):
    __tablename__ = "manga_poster_file"

    type: Mapped[str] = mapped_column(String, nullable=True)
    poster_uuid: Mapped[str] = mapped_column(ForeignKey("manga_poster.uuid", ondelete="CASCADE"), nullable=False)

    poster: Mapped["SQLPoster"] = relationship("Poster", back_populates="files")