from typing import List, Optional

from kanwoo import db
from kanwoo.models import Base

from sqlalchemy import Integer, Text, ForeignKey, DateTime, select, func, and_, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property, query_expression
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from datetime import datetime, timezone

class Vote(Base):
    __tablename__ = "vote"

    comment_id: Mapped[int] = mapped_column(Integer, ForeignKey("comment.id"), primary_key=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey('profile.id'), primary_key=True)
    vote: Mapped[int] = mapped_column()

    comment: Mapped["Comment"] = relationship()
    profile: Mapped["Profile"] = relationship()

    __table_args__ = (
        UniqueConstraint("comment_id", "profile_id", name="uq_comment_vote"),
    )


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey('profile.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    thread_root_id: Mapped[int] = mapped_column(ForeignKey("comment.id"), nullable=True)
    subthread_root_id: Mapped[int] = mapped_column(ForeignKey("comment.id"), nullable=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("comment.id"), nullable=True)
    depth: Mapped[int] = mapped_column(default=1, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(default=lambda _: False)

    creator: Mapped["User"] = relationship('Profile', backref='comments')
    parent: Mapped["Comment"] = relationship("Comment", primaryjoin="Comment.parent_id==Comment.id", back_populates="replies", remote_side=[id])
    replies: Mapped[List["Comment"]] = relationship("Comment", primaryjoin="Comment.id==Comment.parent_id", back_populates="parent", uselist=True)
    
    # manga: Mapped["Manga"] = relationship("Manga", secondary="manga_comment", back_populates="comments")
    # chapter: Mapped["Chapter"] = relationship("Chapter", secondary="chapter_comments", back_populates="comments")
    # post: Mapped["Post"] = relationship("Post", secondary="post_comment", back_populates="comments")

    up_votes: Mapped[int] = column_property(
        select(func.count(Vote.comment_id))
        .where(and_(Vote.comment_id == id, Vote.vote == 1))
        .correlate_except(Vote)
        .scalar_subquery()
    )

    down_votes: Mapped[int] = column_property(
        select(func.count(Vote.comment_id))
        .where(and_(Vote.comment_id == id, Vote.vote == -1))
        .correlate_except(Vote)
        .scalar_subquery()
    )

    replies_count: Mapped[int] = query_expression()
    user_vote: Mapped[Optional[int]] = query_expression()


    @hybrid_property
    def reply_to(self):
        return self.parent.creator


class MangaComment(Base):
    __tablename__ = 'manga_comment'

    manga_id: Mapped[int] = mapped_column(ForeignKey('manga.id'), primary_key=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey('comment.id'), primary_key=True)

class ChapterComment(Base):
    __tablename__ = 'chapter_comment'

    chapter_id: Mapped[int] = mapped_column(ForeignKey('chapter.id'), primary_key=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey('comment.id'), primary_key=True)


# class PostComment(Base):
#     __tablename__ = 'post_comment'
#
#     post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False, primary_key=True)
#     comment_id: Mapped[int] = mapped_column(ForeignKey('comment.id'), nullable=False, primary_key=True)