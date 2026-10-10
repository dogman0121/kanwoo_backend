from dependency_injector.wiring import Provide, inject
from flask import request

from kanwoo import AppContainer, respond
from kanwoo.manga.services import MangaService
from kanwoo.chapter.services import ChapterService
from kanwoo.profile.middleware import profile_required
from kanwoo.comment.services import CommentService
from kanwoo.comment.schemas import GetCommentSchema, GetCommentContextSchema

@profile_required(optional=True)
@inject
def get_preview_handler(
    current_profile,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
):
    comment_type = request.args.get("target_type")
    entity_id = request.args.get("target_id", type=str)

    if comment_type == "manga":
        manga = manga_service.user_get_manga_by_slug(current_profile, entity_id)
        comments, cursor, has_more, total_count = comment_service.user_get_manga_comments_preview(current_profile, manga)
    elif comment_type == "chapter":
        chapter = chapter_service.user_get_chapter_by_id(current_profile, int(entity_id))
        comments, cursor, has_more, total_count = comment_service.user_get_chapter_comments_preview(current_profile, chapter)
    elif comment_type == "post":
        raise NotImplementedError()

    comments_contexts = [comment_service.user_get_comment_context(current_profile, com) for com in comments]

    return respond(
        data=GetCommentSchema().dump(comments, many=True),
        context=GetCommentContextSchema().dump(comments_contexts, many=True),
        cursor=cursor,
        has_more=has_more,
        metadata={"total_count": total_count}
    )