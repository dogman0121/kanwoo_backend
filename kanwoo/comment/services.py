from kanwoo.database import DBTransaction
from kanwoo.profile.entity import AnonymousProfile

from .repositories import CommentRepository
from .permissions import CommentPolicy
from .dto import CommentCreateDTO
from .exceptions import CommentNotFoundException
from .models import Comment, MangaComment, ChapterComment

class CommentService:

    def __init__(
        self,
        comment_repo: CommentRepository,
        comment_policy: CommentPolicy,
        db_transaction: DBTransaction
    ):
        self.comment_repo = comment_repo
        self.comment_policy = comment_policy
        self.db_trasaction = db_transaction

    def user_get_comment_by_id(self, profile, comment_id):
        comment = self.comment_repo.get_comment_by_id_from_user(profile, comment_id)

        if comment is None:
            raise CommentNotFoundException()

        return comment

    def user_create_manga_comment(self, profile, create_comment_dto: CommentCreateDTO):
        with self.db_trasaction:
            comment = Comment(
                text=create_comment_dto.text,
                creator_id=profile.id
            )

            self.comment_repo.create_comment(comment)

            self.db_trasaction.flush()

            manga_comment = MangaComment(
                manga_id=create_comment_dto.manga_id,
                comment_id=comment.id
            )

            self.comment_repo.link_manga_with_comment(manga_comment)

            return comment

    def user_create_chapter_comment(self, profile, create_comment_dto: CommentCreateDTO):
        with self.db_trasaction:
            comment = Comment(
                text=create_comment_dto.text,
                creator_id=profile.id
            )

            self.comment_repo.create_comment(comment)

            self.db_trasaction.flush()
            
            chapter_comment = ChapterComment(
                chapter_id=create_comment_dto.chapter_id,
                comment_id=comment.id
            )

            self.comment_repo.link_chapter_with_comment(chapter_comment)

            return comment

    def user_create_comment_answer(self, profile, comment, create_comment_dto):
        with self.db_trasaction:
            comment = Comment(
                text=create_comment_dto.text,
                parent_id=create_comment_dto.parent_id,
                creator_id=profile.id
            )

            return self.comment_repo.create_comment(comment)

    def user_delete_comment(self, profile, comment):
        with self.db_trasaction:
            self.comment_repo.delete_comment(comment)

    def user_get_comment_answers(self, profile, comment):
        answers = self.comment_repo.get_comment_answers_from_user(profile, comment)

        return answers

    def user_get_manga_comments(self, profile, manga, cursor, limit):
        comments, new_cursor, has_more = self.comment_repo.get_manga_comments(manga, cursor, limit)

        return comments, new_cursor, has_more

    def user_get_manga_comments_preview(self, profile, chapter):
        comments, cursor, has_more, total_count = self.comment_repo.get_manga_comments_preview(chapter, 5)

        return comments, cursor, has_more, total_count

    def user_get_chapter_comments(self, profile, chapter, cursor, limit):
        comments, new_cursor, has_more = self.comment_repo.get_chapter_comments(chapter, cursor, limit)

        return comments, new_cursor, has_more

    def user_get_chapter_comments_preview(self, profile, chapter):
        comments, cursor, has_more, total_count = self.comment_repo.get_chapter_comments_preview(chapter, 5)

        return comments, cursor, has_more, total_count

    def user_update_comment_vote(self, profile, vote):
        pass


