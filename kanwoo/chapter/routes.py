from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.report.dto import ReportCreateDTO
from kanwoo.report.schemas import ReportCreateSchema
from kanwoo.report.services import ReportService
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.reading_progress.dto import UpdateReadingProgressDTO

from .permissions import ChapterPolicy
from .services import ChapterService
from .schemas import (
    ChapterReadingProgressSchema, 
    ChapterUpdateReadingProgressSchema,
)

from .handlers import (
    get_chapter_handler,
    get_last_added_chapters_handler,
    get_chapters_list_handler
)

bp = Blueprint('chapters', __name__, url_prefix='/chapters')

bp.add_url_rule("", methods=["GET"], view_func=get_chapters_list_handler)
bp.add_url_rule("/<int:chapter_id>", view_func=get_chapter_handler, methods=["GET"])
bp.add_url_rule("/last_added", view_func=get_last_added_chapters_handler, methods=["GET"])

@bp.route("/<int:chapter_id>", methods=["DELETE"])
@profile_required()
@inject
def delete_chapter_route(
    current_profile, 
    chapter_id,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):
    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id)

    chapter_service.user_delete_chapter(current_profile, chapter)

    return respond(data={"sucess": True})

@bp.route("/<int:chapter_id>/permissions", methods=["GET"])
@profile_required(optional=True)
@inject
def get_chapter_permissions_route(
    current_profile, 
    chapter_id,
    chapter_policy: ChapterPolicy = Provide[AppContainer.chapter_container.chapter_policy],
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):
    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id)

    return respond(data={"edit": chapter_policy.can_edit(current_profile, chapter)})


@bp.route("/<int:chapter_id>/progress", methods=["GET"])
@profile_required()
@inject
def get_chapter_progress_route(
    current_profile, 
    chapter_id,
    reading_progress_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service],
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):
    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id)

    reading_progress = reading_progress_service.user_get_chapter_progress(current_profile, chapter)

    return respond(data=ChapterReadingProgressSchema().dump(reading_progress))

@bp.route("/<int:chapter_id>/progress", methods=["POST"])
@profile_required()
@inject
def update_chapter_progress_route(
    current_profile, 
    chapter_id,
    reading_progress_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service],
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):
    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id)

    reading_progress_data = ChapterUpdateReadingProgressSchema().load(request.json)

    reading_progress_dto = UpdateReadingProgressDTO(
        page=reading_progress_data.get("page")
    )

    reading_progress_service.user_update_chapter_progress(current_profile, chapter, reading_progress_dto)

    return respond(data={"success": True})


@bp.route("/<int:chapter_id>/reports", methods=["POST"])
@profile_required(optional=True)
@inject
def create_report_route(
    current_profile,
    chapter_id,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
    report_service: ReportService = Provide[AppContainer.report_container.report_service]
):
    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id) 
    
    report_data = ReportCreateSchema().load(request.json)

    report_dto = ReportCreateDTO(
        type_id=report_data.get("type"),
        comment=report_data.get("comment")
    )

    report_service.user_create_chapter_report(current_profile, chapter, report_dto)

    return respond(data={"success": True})


# @bp.get("/<int:chapter_id>/comments")
# @profile_required(optional=True)
# @pagination
# @inject
# def get_chapter_comments_route(
#     current_profile,
#     chapter_id,
#     chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
#     comment_service: CommentService = Provide[AppContainer.comment_container.comment_service],
#     cursor = None,
#     limit = 20
# ):
#     chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id, by_link=True)

#     comments, new_cursor, has_more = comment_service.user_get_chapter_comments(current_profile, chapter, cursor=cursor, limit=limit)

#     return respond(
#         data=CommentSchema().dump(comments, many=True), 
#         cursor=new_cursor, 
#         has_more=has_more,
#         limit=limit
#     )


# @bp.get("/<int:chapter_id>/comments/preview")
# @profile_required(optional=True)
# @inject
# def get_chapter_comments_preview_route(
#     current_profile,
#     chapter_id,
#     chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
#     comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
# ):
#     chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id, by_link=True)
    
#     comments, cursor, has_more, total_count = comment_service.user_get_chapter_comments_preview(current_profile, chapter)

#     return respond(
#         data=CommentSchema().dump(comments, many=True),
#         cursor=cursor,
#         has_more=has_more,
#         metadata={"total_count": total_count}
#     )