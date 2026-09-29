from sqlalchemy import select, desc, func
from typing import Optional
from kanwoo.repositories import BaseRepository
from kanwoo.models import cursor_paginate

from .models import Comment, MangaComment, ChapterComment

class CommentRepository(BaseRepository):
    
    def get_comment_by_id_from_user(self, profile, comment_id):
        return self.db_session.execute(
            select(Comment)
            .filter(Comment.id==comment_id)
        ).scalar()
    

    def create_comment(self, comment):
        comment.add()

        return comment
    
    def link_manga_with_comment(self, manga_comment):
        manga_comment.add()

        return manga_comment
    
    def link_chapter_with_comment(self, chapter_comment):
        chapter_comment.add()

        return chapter_comment
    
    def delete_comment(self, comment):
        comment.delete()

    def get_comment_answers_from_user(self, profile, comment):
        results = self.db_session.execute(
            select(Comment)
            .filter(
                Comment.parent_id==comment.id,
                Comment.is_deleted==False
            )
            .order_by(desc(Comment.created_at))
        ).scalars().all()

        return results
    
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
    
