from dependency_injector.wiring import inject, Provide
from flask import request

from kanwoo import AppContainer, respond
from kanwoo.exceptions import ApiBadRequest
from kanwoo.profile.middleware import profile_required
from kanwoo.comment.services import CommentService
from kanwoo.comment.schemas import CreateCommentSchema, GetCommentSchema, GetCommentContextSchema
from kanwoo.comment.dto import CreateCommentDTO

@profile_required()
@inject
def reply_comment_handler(
    current_profile,
    comment_id,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
):
    comment = comment_service.user_get_comment_by_id(current_profile, comment_id)

    comment_create_schema = CreateCommentSchema().load(request.json)

    comment_create_dto = CreateCommentDTO(
        text = comment_create_schema.get("text"),
    )

    reply = comment_service.user_create_comment_reply(current_profile, comment, comment_create_dto)
    reply_context=  comment_service.user_get_comment_context(current_profile, reply)
    
    return respond(
        data=GetCommentSchema().dump(reply),
        context=GetCommentContextSchema().dump(reply_context)
    )