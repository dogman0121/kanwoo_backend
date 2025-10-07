from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import storage
from app.models import Base, File
from datetime import datetime


class TeamMember(Base):
    __tablename__ = 'team_member'

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

class TeamAvatar(Base, File):
    __tablename__ = 'team_avatar'

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

class TeamPermission(Base):
    __tablename__ = 'team_permission'

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), primary_key=True)
    rule: Mapped[int] = mapped_column(String, primary_key=True)

class TeamLink(Base):
    __tablename__ = 'team_link'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    name: Mapped[str] = mapped_column()
    link: Mapped[str] = mapped_column(String)

class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    about: Mapped[str] = mapped_column(nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=True, default=lambda x: datetime.utcnow())

    links: Mapped[list[TeamLink]] = relationship(uselist=True)
    members: Mapped[list[TeamMember]] = relationship(backref="team", uselist=True)
    avatar: Mapped["TeamAvatar"] = relationship()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "about": self.about,
            "avatar": storage.get(f"/team/{self.id}/{self.poster.uuid}.{self.poster.ext}", ) if self.poster else None,
        }