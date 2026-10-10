from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required
from kanwoo.comment.services import CommentService
from kanwoo.comment.schemas import GetCommentSchema

@profile_required(optional=None)
@inject
def get_comment_handler(
    current_profile,
    comment_id,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
):
    comment = comment_service.user_get_comment_by_id(current_profile, comment_id)

    return respond(data=GetCommentSchema().dump(comment))