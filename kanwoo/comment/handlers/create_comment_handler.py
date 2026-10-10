from dependency_injector.wiring import inject, Provide
from flask import request

from kanwoo import AppContainer, respond
from kanwoo.exceptions import ApiBadRequest
from kanwoo.profile.middleware import profile_required
from kanwoo.chapter.services import ChapterService
from kanwoo.manga.services import MangaService
from kanwoo.comment.services import CommentService
from kanwoo.comment.schemas import CreateCommentSchema, GetCommentSchema, GetCommentContextSchema
from kanwoo.comment.dto import CreateCommentDTO

@profile_required()
@inject
def create_comment_handler(
    current_profile,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
):

    comment_create_schema = CreateCommentSchema().load(request.json)

    comment_create_dto = CreateCommentDTO(
        text = comment_create_schema.get("text")
    )

    if "manga_id" in comment_create_schema:
        manga = manga_service.user_get_manga_by_slug(current_profile, comment_create_schema.get("manga_id"))

        comment = comment_service.user_create_manga_comment(current_profile, manga, comment_create_dto)
    elif "chapter_id" in comment_create_schema:
        chapter = chapter_service.user_get_chapter_by_id(current_profile, comment_create_schema.get("chapter_id"))

        comment = comment_service.user_create_chapter_comment(current_profile, chapter, comment_create_dto)
    else:
        raise ApiBadRequest({
            "message": ["chapter_id or manga_slug must be not null."]
        })

    comment_context = comment_service.user_get_comment_context(current_profile, comment)

    return respond(
        data=GetCommentSchema().dump(comment),
        context=GetCommentContextSchema().dump(comment_context)
    )