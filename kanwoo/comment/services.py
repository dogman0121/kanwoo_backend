from typing import List

from kanwoo.exceptions import ApiBadRequest, ApiNotFound, ApiForbidden
from kanwoo.database import DBTransaction
from kanwoo.profile.entity import AnonymousProfile
from kanwoo.profile.models import Profile

from .repositories import CommentRepository
from .permissions import CommentPolicy
from .dto import CreateCommentDTO, SubthreadDTO, CommentContextDTO, CommentViewerContextDTO, SubthreadContextDTO
from .models import Comment

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
        comment = self.comment_repo.get_comment_by_id_from_user(actor.id, comment_id)

        if comment is None:
            raise ApiNotFound()

        return comment

    def user_create_manga_comment(self, actor, manga, create_comment_dto: CreateCommentDTO):
        with self.db_transaction:
            comment = Comment(
                text=create_comment_dto.text,
                creator_id=actor.id
            )
            self.comment_repo.create_comment(comment)

            self.db_transaction.flush()

            self.comment_repo.link_comment_with_manga(comment.id, manga.id)

        return comment

    def user_create_chapter_comment(self, actor, chapter, create_comment_dto: CreateCommentDTO):
        with self.db_transaction:
            comment = Comment(
                text=create_comment_dto.text,
                creator_id=actor.id
            )
            comment.add()

            self.db_transaction.flush()
            
            self.comment_repo.link_comment_with_chapter(comment.id, chapter.id)

        return comment

    def user_create_comment_reply(self, actor, parent_comment, create_comment_dto):
        with self.db_transaction:
            comment = Comment(
                text=create_comment_dto.text,
                parent_id=parent_comment.id,
                creator_id=actor.id,
                depth=parent_comment.depth + 1
            )

            if parent_comment.depth == 2:
                comment.subthread_root_id = parent_comment.id

            if parent_comment.depth > 2:
                comment.subthread_root_id = parent_comment.subthread_root_id

            self.comment_repo.create_comment(comment)


        return comment

    def user_delete_comment(self, actor, comment):
        with self.db_transaction:
            if not(self.comment_policy.can_delete(actor, comment)):
                raise ApiForbidden()
            
            self.comment_repo.delete_comment(comment)

    def user_get_comment_replies(self, actor: AnonymousProfile | Profile, comment, cursor, limit):

        return self.comment_repo.get_comment_replies(actor.id, comment.id, cursor, limit)

    def user_get_manga_comments(self, actor, manga, cursor, limit):
        
        return self.comment_repo.get_manga_comments(actor.id, manga.id, cursor, limit)

    def user_get_manga_comments_preview(self, actor, manga):
        PREVIEW_SIZE = 5
        comments, cursor, has_more, total_count = self.comment_repo.get_manga_comments_preview(actor.id, manga.id, PREVIEW_SIZE)

        return comments, cursor, has_more, total_count

    def user_get_chapter_comments(self, actor, chapter, cursor, limit):
        comments, new_cursor, has_more = self.comment_repo.get_chapter_comments(actor.id, chapter.id, cursor, limit)

        return comments, new_cursor, has_more

    def user_get_chapter_comments_preview(self, actor, chapter):
        PREVIEW_SIZE = 5
        comments, cursor, has_more, total_count = self.comment_repo.get_chapter_comments_preview(actor.id, chapter.id, PREVIEW_SIZE)

        return comments, cursor, has_more, total_count

    def user_delete_comment_vote(self, actor, comment):
        with self.db_transaction:
            return self.comment_repo.delete_comment_vote(actor.id, comment.id)

    def user_update_comment_vote(self, actor, comment, vote):
        with self.db_transaction:
            return self.comment_repo.update_comment_vote(actor.id, comment.id, vote)

    def user_get_subthread_discussion(self, actor, comment, cursor, limit):
        discussion, ccursor, has_more = self.comment_repo.get_subthread_discussion(actor.id, comment.id, cursor, limit)

        return discussion, ccursor, has_more

    def user_get_comment_subthreads(self, actor, comment, cursor, limit):
        if comment.depth != 1:
            raise ApiBadRequest({"comment_id": ["Comment is already in subthread"]})

        comments, subthreads_cursor, subthreads_has_more = self.comment_repo.get_comment_replies(actor.id, comment.id, cursor, limit)

        subthreads = []
        for thread in comments:
            discussion, ccursor, dhas_more = self.comment_repo.get_subthread_discussion(actor.id, thread.id)
            subthreads.append(SubthreadDTO(
                root_comment=thread,
                discussion=discussion,
                discussion_pagination={
                    "cursor": ccursor,
                    "has_more": dhas_more
                }
            ))

        return subthreads, subthreads_cursor, subthreads_has_more

    def user_get_comment_context(self, actor, comment):
        return CommentContextDTO(
            viewer=CommentViewerContextDTO(
                vote=comment.user_vote
            )
        )

    def user_get_comments_list_contexts(self, actor, comments: List[Comment]):
        contexts = []

        for com in comments:
            contexts.append(
                CommentContextDTO(
                    viewer=CommentViewerContextDTO(
                        vote=com.user_vote
                    )
                )
            )

        return contexts

    def user_get_subthread_context(self, actor, subthread: SubthreadDTO):
        context = SubthreadContextDTO(
            root_comment=self.user_get_comment_context(actor, subthread.root_comment),
            discussion=[self.user_get_comment_context(actor, c) for c in subthread.discussion]
        )

        return context
