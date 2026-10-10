from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.middleware import pagination
from kanwoo.profile.middleware import profile_required
from kanwoo.comment.services import CommentService
from kanwoo.comment.schemas import GetSubthreadSchema, GetSubthreadContextSchema

@profile_required(optional=True)
@pagination
@inject
def get_comment_subthreads_handler(
    current_profile,
    comment_id,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service],
    cursor=None,
    limit=5
):
    comment = comment_service.user_get_comment_by_id(current_profile, comment_id)

    subthreads, new_cursor, has_more = comment_service.user_get_comment_subthreads(current_profile, comment, cursor, limit)

    subthreads_contexts = [comment_service.user_get_subthread_context(current_profile, thread) for thread in subthreads]

    return respond(
        data=GetSubthreadSchema().dump(subthreads, many=True),
        context=GetSubthreadContextSchema().dump(subthreads_contexts, many=True),
        cursor=new_cursor,
        has_more=has_more
    )