from dependency_injector.wiring import inject, Provide

from kanwoo import respond, AppContainer
from kanwoo.profile.middleware import profile_required
from kanwoo.comment.services import CommentService
from kanwoo.comment.schemas import GetCommentSchema


@profile_required(optional=True)
@inject
def get_comment_replies_handler(
    current_profile,
    comment_id,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
):
    comment = comment_service.user_get_comment_by_id(current_profile, comment_id)

    answers = comment_service.user_get_comment_answers(current_profile, comment)

    return respond(data=GetCommentSchema().dump(answers, many=True))