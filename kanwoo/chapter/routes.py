from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.report.dto import ReportCreateDTO
from kanwoo.report.schemas import ReportCreateSchema
from kanwoo.report.services import ReportService
from kanwoo.reading_progress.dto import ReadingProgressDTO
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.middleware import pagination
from kanwoo.comment.services import CommentService
from kanwoo.comment.schemes import CommentSchema

from .dto import ChapterUpdateDTO
from .permissions import ChapterPolicy
from .services import ChapterService
from .schemas import (
    ChapterSchemaFull, 
    ChapterUpdateSchema, 
    ChapterReadingProgressSchema, 
    ChapterUpdateReadingProgressSchema
)

bp = Blueprint('chapters', __name__, url_prefix='/chapters')

@bp.route("/<int:chapter_id>", methods=["GET"])
@profile_required(optional=True)
@inject
def get_chapter_route(
    current_profile, 
    chapter_id,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):
    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id, by_link=True)

    return respond(data=ChapterSchemaFull().dump(chapter))

@bp.route("/<int:chapter_id>", methods=["PUT"])
@profile_required()
@inject
def update_chapter_route(
    current_profile, 
    chapter_id,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service]
):  
    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id)

    update_data = ChapterUpdateSchema().load({
        "name": request.form.get("name"),
        "chapter": request.form.get("chapter"),
        "privacy": request.form.get("privacy"),
        "pages": request.files.getlist("pages"),
        "pages_order": request.form.get("pages_order")
    })

    update_dto = ChapterUpdateDTO(
        name=update_data.get("name"),
        chapter=update_data.get("chapter"),
        privacy=update_data.get("privacy"),
        pages=update_data.get("pages"),
        pages_order=update_data.get("pages_order")
    )
    
    chapter = chapter_service.user_update_chapter(current_profile, chapter, update_dto)

    return respond(data=ChapterSchemaFull().dump(chapter))

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

    reading_progress_dto = ReadingProgressDTO(
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


@bp.route("/<int:chapter_id>/comments", methods=["GET"])
@profile_required(optional=True)
@pagination
@inject
def get_chapter_comments(
    current_profile,
    chapter_id,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service],
    last_id: int = 0,
    limit: int = 20
):
    chapter = chapter_service.user_get_chapter_by_id(current_profile, chapter_id, by_link=True)

    comments, total_count, last_id = comment_service.user_get_chapter_comments(current_profile, chapter, last_id, limit)

    return respond(
        data=CommentSchema().dump(comments, many=True), 
        last_id=last_id, 
        total_count=total_count, 
        limit=limit
    )
