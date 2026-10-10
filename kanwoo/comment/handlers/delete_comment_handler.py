from dependency_injector.wiring import inject, Provide

from kanwoo import respond, AppContainer
from kanwoo.profile.middleware import profile_required
from kanwoo.comment.services import CommentService

@profile_required()
@inject
def delete_comment_handler(
    current_profile,
    comment_id,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
):
    comment = comment_service.user_get_comment_by_id(current_profile, comment_id)    

    comment_service.user_delete_comment(current_profile, comment)

    return respond(data={"success": True})