from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer, respond
from kanwoo.middleware import pagination
from kanwoo.profile.middleware import profile_required
from kanwoo.comment.services import CommentService
from kanwoo.comment.schemas import GetDiscussionCommentSchema, GetDiscussionCommentContextSchema


@profile_required(optional=True)
@pagination
@inject
def get_subthread_discussion_handler(
    current_profile,
    subthread_id, 
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service],
    cursor=None,
    limit=10
):
    comment = comment_service.user_get_comment_by_id(current_profile, subthread_id)

    comments, new_cursor, has_more = comment_service.user_get_discussion_comments(current_profile, comment, cursor, limit)
    comments_contexts = comment_service.user_get_discussiob_comments_contexts()

    return respond(
        data=GetDiscussionCommentSchema().dump(comments, many=True),
        context=GetDiscussionCommentContextSchema().dump(comments_contexts, many=True),
        cursor=new_cursor,
        has_more=has_more
    )