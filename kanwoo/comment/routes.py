from flask import Blueprint, request
from dependency_injector.wiring import inject, Provide

from kanwoo.utils import respond
from kanwoo.containers import AppContainer
from kanwoo.profile.middleware import profile_required
from kanwoo.exceptions import ApiBadRequest
from kanwoo.report.services import ReportService
from kanwoo.report.schemas import ReportCreateSchema
from kanwoo.report.dto import ReportCreateDTO

from .schemes import CommentCreateSchema, CommentSchema, CommentPatchVoteSchema
from .dto import CommentCreateDTO
from .services import CommentService

bp = Blueprint("comment", __name__)

@bp.route("", strict_slashes=False, methods=["GET"])
def get_comments_route():
    raise NotImplementedError()

@bp.route("", strict_slashes=False, methods=["POST"])
@profile_required()
@inject
def create_comment_route(
    current_profile,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
):
    
    comment_create_schema = CommentCreateSchema().load(request.json)

    comment_create_dto = CommentCreateDTO(
        text = comment_create_schema.get("text"),
        parent_id = comment_create_schema.get("parent"),
        chapter_id = comment_create_schema.get("chapter"),
        manga_id = comment_create_schema.get("manga")
    )

    if comment_create_dto.manga_id:
        comment = comment_service.user_create_manga_comment(current_profile, comment_create_dto)
    elif comment_create_dto.chapter_id:
        comment = comment_service.user_create_chapter_comment(current_profile, comment_create_dto)
    elif comment_create_dto.parent_id:
        parent_comment = comment_service.user_get_comment_by_id(current_profile, comment_create_dto.parent_id)

        comment = comment_service.user_create_comment_answer(current_profile, parent_comment, comment_create_dto)
    else:
        raise ApiBadRequest({
            "message": ["Manga or Chapter or Parent must be not null."]
        })
    
    return respond(data=CommentSchema().dump(comment))

@bp.route("/<int:comment_id>", methods=["GET"])
@profile_required(optional=None)
@inject
def get_comment_route(
    current_profile,
    comment_id,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
):
    comment = comment_service.user_get_comment_by_id(current_profile, comment_id)

    return respond(data=CommentSchema().dump(comment))


@bp.route("/<int:comment_id>", methods=["DELETE"])
@profile_required()
@inject
def delete_comment_route(
    current_profile,
    comment_id,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
):
    comment = comment_service.user_get_comment_by_id(current_profile, comment_id)    

    comment_service.user_delete_comment(current_profile, comment)

    return respond(data={"success": True})
    


@bp.route("/<int:comment_id>/answers", methods=["GET"])
@profile_required(optional=True)
@inject
def get_comment_answers(
    current_profile,
    comment_id,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
):
    comment = comment_service.user_get_comment_by_id(current_profile, comment_id)

    answers = comment_service.user_get_comment_answers(current_profile, comment)

    return respond(data=CommentSchema().dump(answers, many=True))


@bp.route("/<int:comment_id>/votes", methods=["PATCH"])
@profile_required()
@inject
def update_comment_vote(
    current_profile,
    comment_id,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service]
):
    vote_schema = CommentPatchVoteSchema().load(request.json)

    chosen_vote = vote_schema.get("vote")

    comment = comment_service.user_get_comment_by_id(current_profile, comment_id)

    comment_service.user_update_comment_vote(current_profile, comment, chosen_vote)

    return respond(data={"success": True})

    
@bp.route("/<int:comment_id>/reports", methods=["POST"])
@profile_required(optional=True)
@inject
def report_comment_route(
    current_profile,
    comment_id,
    comment_service: CommentService = Provide[AppContainer.comment_container.comment_service],
    report_service: ReportService = Provide[AppContainer.report_container.report_service]

):
    comment = comment_service.user_get_comment_by_id(current_profile, comment_id)

    create_report_schema = ReportCreateSchema().load(request.json)

    create_report_dto = ReportCreateDTO(
        type_id=create_report_schema.get("type"),
        comment=create_report_schema.get("comment")
    )

    report_service.user_create_comment_report(current_profile, comment, create_report_dto)

    return respond(data={"success": True})