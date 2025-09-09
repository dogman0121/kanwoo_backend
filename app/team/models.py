from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import storage
from app.models import Base, File
from datetime import datetime

class TeamMember(Base):
    __tablename__ = 'team_member'

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

class TeamPoster(Base, File):
    __tablename__ = 'team_poster'

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), primary_key=True)

class TeamPermission(Base):
    __tablename__ = 'team_permission'

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), primary_key=True)
    rule: Mapped[int] = mapped_column(String, primary_key=True)

class TeamLink(Base):
    __tablename__ = 'team_link'

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), primary_key=True)
    type: Mapped[str] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String)

class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    about: Mapped[str] = mapped_column(nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=True, default=lambda x: datetime.utcnow())

    members: Mapped[list[TeamMember]] = relationship(backref="team", uselist=True)
    poster: Mapped["TeamPoster"] = relationship()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "about": self.about,
            "poster": storage.get(f"/team/{self.id}/{self.poster.uuid}.{self.poster.ext}", ) if self.poster else None,
        }