from dependency_injector.wiring import inject, Provide
from flask import request

from kanwoo import respond, AppContainer
from kanwoo.profile.middleware import profile_required
from kanwoo.comment.services import CommentService
from kanwoo.comment.schemas import VoteSchema


@profile_required()
@inject
def vote_comment_handler(
    current_profile,
    comment_id,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
):
    vote_schema = VoteSchema().load(request.json)

    chosen_vote = vote_schema.get("vote")

    comment = comment_service.user_get_comment_by_id(current_profile, comment_id)

    vote = comment.user_vote
    if vote == chosen_vote:
        comment_service.user_delete_comment_vote(current_profile, comment)
    else:
        comment_service.user_update_comment_vote(current_profile, comment, chosen_vote)

    return respond(data={"success": True})
