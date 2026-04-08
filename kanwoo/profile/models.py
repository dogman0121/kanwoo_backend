from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from kanwoo.models import Base, File
from datetime import datetime



class ProfileAvatar(Base, File):
    __tablename__ = 'profile_avatar'

    
class ProfilePermission(Base):
    __tablename__ = 'profile_permission'

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), primary_key=True)
    rule: Mapped[int] = mapped_column(String, primary_key=True)

class ProfileLink(Base):
    __tablename__ = 'profile_link'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
    name: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)

class ProfileMemberType(Base):
    __tablename__ = "profile_member_type"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

class ProfileMembers(Base):
    __tablename__ = "profile_member"

    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("profile_member_type.id"))

class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    about: Mapped[str] = mapped_column(nullable=True)
    avatar_uuid: Mapped[str] = mapped_column(ForeignKey("profile_avatar.uuid", ondelete="SET NULL"), nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=True, default=lambda x: datetime.utcnow())
    role: Mapped[int] = mapped_column(nullable=True, default=1)

    links: Mapped[list[ProfileLink]] = relationship(uselist=True)
    avatar: Mapped[ProfileAvatar] = relationship()