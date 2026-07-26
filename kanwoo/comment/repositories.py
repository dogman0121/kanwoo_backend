from sqlalchemy import select, desc

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
    
    def get_manga_comments_from_user(self, profile, manga, last_id, limit):
        query = (
            select(Comment)
            .join(MangaComment, Comment.id == MangaComment.comment_id)
            .order_by(desc(Comment.created_at))
            .filter(MangaComment.manga_id==manga.id)
        )

        results, total_count, new_last_id = cursor_paginate(Comment, self.db_session, query, last_id, limit)

        return results, total_count, new_last_id
    
    def get_chapter_comments_from_user(self, profile, chapter, last_id, limit):
        query = (
            select(Comment)
            .join(ChapterComment, Comment.id == ChapterComment.comment_id)
            .order_by(desc(Comment.created_at))
            .filter(ChapterComment.chapter_id==chapter.id)
        )

        results, total_count, new_last_id = cursor_paginate(Comment, self.db_session, query, last_id, limit)

        return results, total_count, new_last_id
    
    
