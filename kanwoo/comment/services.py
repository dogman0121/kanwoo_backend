from typing import List

from kanwoo.exceptions import ApiBadRequest, ApiNotFound, ApiForbidden
from kanwoo.database import DBTransaction
from kanwoo.profile.entity import AnonymousProfile
from kanwoo.profile.models import Profile

from .repositories import CommentRepository
from .permissions import CommentPolicy
from .dto import CreateCommentDTO, SubthreadDTO, CommentContextDTO, CommentViewerContextDTO
from .models import Comment, ChapterComment

class CommentService:

    def __init__(
        self,
        comment_repo: CommentRepository,
        comment_policy: CommentPolicy,
        db_transaction: DBTransaction
    ):
        self.comment_repo = comment_repo
        self.comment_policy = comment_policy
        self.db_transaction = db_transaction

    def user_get_comment_by_id(self, actor: AnonymousProfile | Profile, comment_id):
        comment = self.comment_repo.get_comment_by_id_from_user(actor, comment_id)

        if comment is None:
            raise ApiNotFound()

        return comment

    def user_create_manga_comment(self, actor, create_comment_dto: CreateCommentDTO):
        with self.db_transaction:
            comment = Comment(
                text=create_comment_dto.text,
                creator_id=actor.id
            )
            self.comment_repo.create_comment(comment)

            self.db_transaction.flush()

            self.comment_repo.link_comment_with_manga(comment, create_comment_dto.manga_id)

        return comment

    def user_create_chapter_comment(self, actor, create_comment_dto: CreateCommentDTO):
        with self.db_transaction:
            comment = Comment(
                text=create_comment_dto.text,
                creator_id=actor.id
            )
            comment.add()

            self.db_trasaction.flush()
            
            chapter_comment = ChapterComment(
                chapter_id=create_comment_dto.chapter_id,
                comment_id=comment.id
            )
            chapter_comment.add()

        return comment

    def user_create_comment_reply(self, actor, parent_comment, create_comment_dto):
        with self.db_trasaction:

            comment = Comment(
                text=create_comment_dto.text,
                parent_id=create_comment_dto.parent_id,
                creator_id=actor.id,
                depth=parent_comment.depth + 1
            )

            if parent_comment.depth == 2:
                comment.subthread_root_id = parent_comment.id

            comment.add()

        return comment

    def user_delete_comment(self, actor, comment):
        with self.db_trasaction:
            if not(self.comment_policy.can_delete(actor, comment)):
                raise ApiForbidden()
            
            self.comment_repo.delete_comment(comment)

    def user_get_comment_replies(self, comment, cursor, limit):
        replies, ccursor, has_more = self.comment_repo.get_comment_replies(comment.id, cursor, limit)

        return replies, ccursor, has_more

    def user_get_manga_comments(self, manga, cursor, limit):
        comments, new_cursor, has_more = self.comment_repo.get_manga_comments(manga, cursor, limit)

        return comments, new_cursor, has_more

    def user_get_manga_comments_preview(self, chapter):
        PREVIEW_SIZE = 5
        comments, cursor, has_more, total_count = self.comment_repo.get_manga_comments_preview(chapter, PREVIEW_SIZE)

        return comments, cursor, has_more, total_count

    def user_get_chapter_comments(self, chapter, cursor, limit):
        comments, new_cursor, has_more = self.comment_repo.get_chapter_comments(chapter, cursor, limit)

        return comments, new_cursor, has_more

    def user_get_chapter_comments_preview(self, chapter):
        PREVIEW_SIZE = 5
        comments, cursor, has_more, total_count = self.comment_repo.get_chapter_comments_preview(chapter, PREVIEW_SIZE)

        return comments, cursor, has_more, total_count

    def user_update_comment_vote(self, actor, vote):
        pass

    def user_get_subthread_discussion(self, comment, cursor, limit):
        discussion, ccursor, has_more = self.comment_repo.get_subthread_discussion(comment.id, cursor, limit)

        return discussion, ccursor, has_more

    def user_get_comment_subthreads(self, comment, cursor, limit):
        if comment.depth != 1:
            raise ApiBadRequest({"comment_id": ["Comment is already in subthread"]})

        comments, ccursor, has_more = self.comment_repo.get_comment_replies(comment.id, cursor, limit)

        subthreads = []
        for thread in comments:
            discussion, ccursor, dhas_more = self.comment_repo.get_subthread_discussion(thread.id)
            subthreads.append(SubthreadDTO(
                root_comment=thread,
                discussion=discussion,
                discussion_pagination={
                    "cursor": ccursor,
                    "has_more": dhas_more
                }
            ))

        return subthreads, ccursor, has_more

    def user_get_comment_context(self, actor, comment):
        return CommentContextDTO(
            viewer=CommentViewerContextDTO(
                vote=comment.user_vote(actor.id)
            )
        )

    def user_get_comments_list_contexts(self, actor, comments: List[Comment]):
        contexts = []

        for com in comments:
            contexts.append(
                CommentContextDTO(
                    viewer=CommentViewerContextDTO(
                        vote=com.user_vote(actor.id)
                    )
                )
            )

        return contexts