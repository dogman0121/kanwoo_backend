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
def get_comments_preview_handler(
    current_profile,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
):
    comments = []
    if "manga_id" in request.args:
        manga = manga_service.user_get_manga_by_slug(current_profile, request.args.get("manga_id"))

        comments, new_cursor, has_more, total_count = comment_service.user_get_manga_comments_preview(current_profile, manga, cursor=cursor, limit=limit)
    elif "chapter_id" in request.args:
        chapter = chapter_service.user_get_chapter_by_id(current_profile, request.args.get("chapter_id", type=int))

        comments, new_cursor, has_more, total_count = comment_service.user_get_chapter_comments_preview(current_profile, chapter, cursor=cursor, limit=limit)
    elif "post_id" in request.args:
        raise NotImplementedError()

    comments_contexts = [comment_service.user_get_comment_context(current_profile, c) for c in comments]

    return respond(
        data=GetCommentSchema().dump(comments, many=True),
        context=GetCommentContextSchema().dump(comments_contexts, many=True),
        cursor=new_cursor,
        has_more=has_more,
        metadata={"total_count": total_count}
    )