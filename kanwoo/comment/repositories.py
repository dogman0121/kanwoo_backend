from sqlalchemy import select, desc, func

from kanwoo.repositories import BaseRepository
from kanwoo.models import cursor_paginate

from .models import Comment, MangaComment, ChapterComment, Vote

class CommentRepository(BaseRepository):
    
    def get_comment_by_id_from_user(self, profile, comment_id):
        return self.db_session.execute(
            select(Comment).filter(Comment.id==comment_id)
        ).scalar_one_or_none()

    def create_comment(self, comment):
        self.db_session.add(comment)
    
    def delete_comment(self, comment):
        self.db_session.delete(comment)

    def link_comment_with_manga(self, comment, manga_id):
        manga_comment = MangaComment(
            comment_id = comment.id,
            manga_id=manga_id
        )

        self.db_session.add(manga_comment)

    def link_comment_with_chapter(self, comment, chapter_id):
        chapter_comment = MangaComment(
            comment_id = comment.id,
            manga_id=chapter_id
        )

        self.db_session.add(chapter_comment)

    def get_comment_replies(self, comment_id, cursor, limit):
        q = select(Comment).filter(
            Comment.parent_id==comment_id,
            Comment.is_deleted==False
        )

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
    
    def get_manga_comments(self, manga, cursor, limit: int):
        query = (
            select(Comment)
            .join(MangaComment, Comment.id == MangaComment.comment_id)
            .filter(MangaComment.manga_id==manga.id)
            .filter(Comment.parent_id == None)
        )

        results, new_cursor, has_more = cursor_paginate(
            Comment, 
            self.db_session, 
            query, 
            None,
            cursor=cursor,
            limit=limit,
            direction="desc"
        )

        return results, new_cursor, has_more

    def get_manga_comments_preview(self, chapter, preview_size):
        query = (
            select(Comment)
            .join(MangaComment, Comment.id == MangaComment.comment_id)
            .filter(MangaComment.manga_id==chapter.id)
            .filter(Comment.parent_id == None)
        )

        results, cursor, has_more = cursor_paginate(
            Comment,
            self.db_session,
            query,
            None,
            limit=preview_size,
            direction="desc"
        )
        total_count = self.db_session.execute(select(func.count("*")).select_from(query)).scalar_one()

        return results, cursor, has_more, total_count
    
    def get_chapter_comments(self, chapter, cursor, limit: int):
        query = (
            select(Comment)
            .join(ChapterComment, Comment.id == ChapterComment.comment_id)
            .filter(ChapterComment.chapter_id==chapter.id)
            .filter(Comment.parent_id == None)
        )

        results, new_cursor, has_more = cursor_paginate(
            Comment, 
            self.db_session, 
            query, 
            None,
            cursor=cursor,
            limit=limit,
            direction="desc"
        )

        return results, new_cursor, has_more

    def get_chapter_comments_preview(self, chapter, preview_size):
        query = (
            select(Comment)
            .join(ChapterComment, Comment.id == ChapterComment.comment_id)
            .filter(ChapterComment.chapter_id==chapter.id)
            .filter(Comment.parent_id == None)
        )

        results, cursor, has_more = cursor_paginate(
            Comment,
            self.db_session,
            query,
            None,
            limit=preview_size,
            direction="desc"
        )
        total_count = self.db_session.execute(select(func.count("*")).select_from(query)).scalar_one()

        return results, cursor, has_more, total_count
    
    def get_subthread_discussion(self, subthread_id, cursor=None, limit=5):
        q = select(Comment).filter(
            Comment.subthread_root_id == subthread_id
        )

        results, ccursor, has_more = cursor_paginate(
            Comment,
            self.db_session,
            q,
            sort_field=None,
            cursor=cursor,
            limit=limit
        )

        return results, ccursor, has_more