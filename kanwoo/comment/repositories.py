from typing import Optional

from sqlalchemy import select, desc, func, delete, and_
from sqlalchemy.orm import joinedload, with_expression, aliased
from sqlalchemy.dialects.postgresql import insert

from kanwoo.repositories import BaseRepository
from kanwoo.models import cursor_paginate

from .models import Comment, MangaComment, ChapterComment, Vote

class CommentRepository(BaseRepository):

    def _add_options(self, q, profile_id: Optional[int]):
        child = aliased(Comment, name="child_comment")

        replies_count_expr = (
            select(func.count(child.id))
                .where(child.parent_id == Comment.id)
                .correlate_except(child)
                .scalar_subquery()
        )

        q = q.options(
            with_expression(Comment.replies_count, replies_count_expr),
        )

        if profile_id:
            user_vote_expr = (
                select(Vote.vote)
                .where(and_(
                    Vote.comment_id == Comment.id,
                    Vote.profile_id == profile_id,
                ))
                .correlate_except(Vote)
                .scalar_subquery()
            )

            q = q.options(
                with_expression(
                    Comment.user_vote, user_vote_expr
                )
            )

        return q
    
    def get_comment_by_id_from_user(self, profile_id: Optional[int], comment_id: int):
        q = (
            select(Comment)
            .filter(
                Comment.id==comment_id
            )
        )

        q = self._add_options(q, profile_id)

        return self.db_session.execute(q).scalar()

    def create_comment(self, comment):
        self.db_session.add(comment)
    
    def delete_comment(self, comment):
        self.db_session.delete(comment)

    def link_comment_with_manga(self, comment_id: int, manga_id: int):
        manga_comment = MangaComment(
            comment_id = comment_id,
            manga_id=manga_id
        )

        self.db_session.add(manga_comment)

    def link_comment_with_chapter(self, comment_id: int, chapter_id: int):
        chapter_comment = ChapterComment(
            comment_id = comment_id,
            chapter_id=chapter_id
        )

        self.db_session.add(chapter_comment)

    def get_comment_replies(self, profile_id: Optional[int], comment_id: int, cursor, limit):
        q = select(Comment).filter(
            Comment.parent_id==comment_id,
            Comment.is_deleted==False
        )

        q = self._add_options(q, profile_id)

        results, ccursor, has_more = cursor_paginate(
            Comment,
            self.db_session,
            q,
            sort_field=None,
            cursor=cursor,
            limit=limit,
            direction="desc"
        )

        return results, ccursor, has_more
    
    def get_manga_comments(self, profile_id: Optional[int], manga_id: int, cursor: dict, limit: int):
        q = (
            select(Comment)
            .join(MangaComment, Comment.id == MangaComment.comment_id)
            .filter(MangaComment.manga_id==manga_id)
            .filter(Comment.parent_id == None)
        )

        q = self._add_options(q, profile_id)

        results, new_cursor, has_more = cursor_paginate(
            Comment, 
            self.db_session, 
            q, 
            None,
            cursor=cursor,
            limit=limit,
            direction="desc"
        )

        return results, new_cursor, has_more

    def get_manga_comments_preview(self, profile_id: Optional[int], manga_id: int, preview_size: int):
        q = (
            select(Comment)
            .join(MangaComment, Comment.id == MangaComment.comment_id)
            .filter(MangaComment.manga_id==manga_id)
            .filter(Comment.parent_id == None)
        )

        q = self._add_options(q, profile_id)

        results, cursor, has_more = cursor_paginate(
            Comment,
            self.db_session,
            q,
            None,
            limit=preview_size,
            direction="desc"
        )
        total_count = self.db_session.execute(select(func.count("*")).select_from(q)).scalar_one()

        return results, cursor, has_more, total_count
    
    def get_chapter_comments(self, profile_id: Optional[int], chapter_id: int, cursor: dict, limit: int):
        q = (
            select(Comment)
            .join(ChapterComment, Comment.id == ChapterComment.comment_id)
            .filter(ChapterComment.chapter_id==chapter_id)
            .filter(Comment.parent_id == None)
        )

        q = self._add_options(q, profile_id)

        results, new_cursor, has_more = cursor_paginate(
            Comment, 
            self.db_session, 
            q, 
            None,
            cursor=cursor,
            limit=limit,
            direction="desc"
        )

        return results, new_cursor, has_more

    def get_chapter_comments_preview(self, profile_id: Optional[int], chapter_id: int, preview_size: int):
        q = (
            select(Comment)
            .join(ChapterComment, Comment.id == ChapterComment.comment_id)
            .filter(ChapterComment.chapter_id==chapter_id)
            .filter(Comment.parent_id == None)
        )

        q = self._add_options(q, profile_id)

        results, cursor, has_more = cursor_paginate(
            Comment,
            self.db_session,
            q,
            None,
            limit=preview_size,
            direction="desc"
        )
        total_count = self.db_session.execute(select(func.count("*")).select_from(q)).scalar_one()

        return results, cursor, has_more, total_count
    
    def get_subthread_discussion(self, profile_id: Optional[int], subthread_id: int, cursor: Optional[dict] = None, limit: int = 3):
        q = select(Comment).filter(
            Comment.subthread_root_id == subthread_id
        )

        q = self._add_options(q, profile_id)

        results, ccursor, has_more = cursor_paginate(
            Comment,
            self.db_session,
            q,
            sort_field=None,
            cursor=cursor,
            limit=limit
        )

        return results, ccursor, has_more

    def get_comment_vote(self, profile_id: int, comment_id: int):
        return self.db_session.execute(select(Vote).filter(Vote.comment_id == comment_id, Vote.profile_id == profile_id)).scalar()

    def delete_comment_vote(self, profile_id: int, comment_id: int):
        return self.db_session.execute(delete(Vote).filter(Vote.comment_id==comment_id, Vote.profile_id == profile_id))

    def update_comment_vote(self, profile_id: int, comment_id: int, vote: int):
        insert_stmt = insert(Vote).values(
            profile_id=profile_id,
            comment_id=comment_id,
            vote=vote
        )

        update_stmt = insert_stmt.on_conflict_do_update(
            "uq_comment_vote",
            set_={"vote": vote}
        )

        self.db_session.execute(update_stmt)