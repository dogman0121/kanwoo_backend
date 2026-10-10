from dependency_injector.wiring import inject, Provide
from flask import request

from kanwoo import AppContainer, respond
from kanwoo.exceptions import ApiBadRequest
from kanwoo.profile.middleware import profile_required
from kanwoo.comment.services import CommentService
from kanwoo.comment.schemas import CreateCommentSchema, GetCommentSchema
from kanwoo.comment.dto import CreateCommentDTO

@profile_required()
@inject
def create_comment_handler(
    current_profile,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
):

    comment_create_schema = CreateCommentSchema().load(request.json)

    comment_create_dto = CreateCommentDTO(
        text = comment_create_schema.get("text"),
        parent_id=None,
        chapter_id = comment_create_schema.get("chapter_id"),
        manga_id = comment_create_schema.get("manga_id")
    )

    if comment_create_dto.manga_id:
        comment = comment_service.user_create_manga_comment(current_profile, comment_create_dto)
    elif comment_create_dto.chapter_id:
        comment = comment_service.user_create_chapter_comment(current_profile, comment_create_dto)
    else:
        raise ApiBadRequest({
            "message": ["chapter_id or manga_slug must be not null."]
        })

    return respond(data=GetCommentSchema().dump(comment))