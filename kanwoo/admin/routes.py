from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.middleware import moderator_required
from kanwoo.utils import respond
from kanwoo.report.services import ReportService
from kanwoo.main.services import FeedbackService
from kanwoo.moderation.services import ModerationService
from kanwoo.moderation.dto import ModerationStatusUpdateDTO
from kanwoo.manga.services import MangaService, MangaSuggestionService
from kanwoo.manga.dto import MangaCreateDTO, NameTranslationDTO

from .dto import AdminMangaFiltersDTO
from .schemas import (
    AdminMainDashboardSchema, 
    AdminMangaSchema, 
    AdminAddModerationStatusSchema, 
    AdminModerationStatusSchema,
    AdminFeedbackSchema,
    AdminChapterReportSchema,
    AdminMangaReportSchema,
    AdminMangaCreateSchema,
    AdminMangaSuggestionSchema
)
from .utils import convert_manga_create_form_into_create_dto, \
    convert_manga_update_form_into_update_dto
from .services import AdminDashboardService, AdminMangaService

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route("/dashboards/main", methods=["GET"])
@moderator_required
@inject
def get_main_dashboard_route(
    current_profile,
    admin_dashboard_service: AdminDashboardService = Provide[AppContainer.admin_container.admin_dashboard_service]
):
    dashboard = admin_dashboard_service.user_get_main_dashboard(current_profile)

    return respond(data=AdminMainDashboardSchema().dump(dashboard))


@bp.route("/manga", methods=["GET"])
@moderator_required
@inject
def get_manga_list_route(
    current_profile,
    admin_manga_service: AdminMangaService = Provide[AppContainer.admin_container.admin_manga_service]
):
    filters_dto = AdminMangaFiltersDTO(
        query=request.args.get("query", None, type=str),
        statuses=request.args.getlist("status")
    )

    manga = admin_manga_service.user_get_manga_list(current_profile, filters_dto)

    return respond(data=AdminMangaSchema().dump(manga, many=True))

@bp.route("/manga", methods=["POST"])
@moderator_required
@inject
def create_manga_route(
    current_profile,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    create_dto = convert_manga_create_form_into_create_dto(request.form, request.files)

    manga = manga_service.user_create_manga(current_profile, create_dto)

    manga_schema = AdminMangaSchema()

    return respond(data=manga_schema.dump(manga))

@bp.route("/manga/<manga_slug>", methods=["GET"])
@moderator_required
@inject
def get_manga_route(
    current_profile,
    manga_slug,
    admin_manga_service: AdminMangaService = Provide[AppContainer.admin_container.admin_manga_service]
):
    manga = admin_manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    manga_schema = AdminMangaSchema()

    return respond(data=manga_schema.dump(manga))


@bp.route("/manga/<manga_slug>", methods=["PUT"])
@moderator_required
@inject
def update_manga_route(
    current_profile,
    manga_slug,
    admin_manga_service: AdminMangaService = Provide[AppContainer.admin_container.admin_manga_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = admin_manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    update_dto = convert_manga_update_form_into_update_dto(request.form, request.files)

    manga = manga_service.user_update_manga(current_profile, manga, update_dto)

    manga_schema = AdminMangaSchema()

    return respond(data=manga_schema.dump(manga))

@bp.route("/manga/suggestions", methods=["GET"])
@moderator_required
@inject
def get_manga_suggestions(
    current_profile,
    manga_suggestion_service: MangaSuggestionService = Provide[AppContainer.manga_container.manga_suggestion_service]
):
    resolved_str = request.args.get("resolved")

    resolved = None
    if resolved_str == "true":
        resolved = True
    elif resolved_str == "false":
        resolved = False
        
    manga_suggestions = manga_suggestion_service.user_get_suggestions(current_profile, resolved)

    return respond(data=AdminMangaSuggestionSchema().dump(manga_suggestions, many=True))

@bp.route("/manga/suggestions/<int:suggestion_id>", methods=["DELETE"])
@moderator_required
@inject
def resolve_manga_suggestions(
    current_profile,
    suggestion_id,
    manga_suggestion_service: MangaSuggestionService = Provide[AppContainer.manga_container.manga_suggestion_service]
):
    manga_suggestion = manga_suggestion_service.user_get_suggestion_by_id(suggestion_id)

    updated_manga_suggestion = manga_suggestion_service.user_resolve_suggestion(current_profile, manga_suggestion)

    return respond(data=AdminMangaSuggestionSchema().load(updated_manga_suggestion, many=True))


@bp.route("/manga/<manga_slug>/moderation", methods=["PUT"])
@moderator_required
@inject
def update_manga_moderation_status_route(
    current_profile,
    manga_slug,
    admin_manga_service: AdminMangaService = Provide[AppContainer.admin_container.admin_manga_service],
    moderation_service: ModerationService = Provide[AppContainer.moderation_container.moderation_service]
):
    moderation_status_data = AdminAddModerationStatusSchema().load(request.json)

    manga = admin_manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    moderation_status_dto = ModerationStatusUpdateDTO(
        status_type_id=moderation_status_data.get("status_type"),
        message=moderation_status_data.get("message")
    )

    moderation_status = moderation_service.user_update_manga_moderation_status(current_profile, manga, moderation_status_dto)

    return respond(data=AdminModerationStatusSchema().dump(moderation_status))


@bp.route("/feedbacks", methods=["GET"])
@moderator_required
@inject
def get_feedbacks_route(
    current_profile,
    feedback_service: FeedbackService = Provide[AppContainer.main_container.feedback_service]
):
    resolved_str = request.args.get("resolved")

    resolved = None
    if resolved_str == "true":
        resolved = True
    elif resolved_str == "false":
        resolved = False

    feedbacks = feedback_service.user_get_feedbacks(current_profile, resolved=resolved)

    return respond(data=AdminFeedbackSchema().dump(feedbacks, many=True))


@bp.route("/feedbacks/<int:feedback_id>", methods=["DELETE"])
@moderator_required
@inject
def resolve_feddback_route(
    current_profile,
    feedback_id,
    feedback_service: FeedbackService = Provide[AppContainer.main_container.feedback_service]
):
    feedback = feedback_service.user_get_feedback_by_id(current_profile, feedback_id)

    feedback = feedback_service.user_resolve_feedback(current_profile, feedback)

    return respond(data=AdminFeedbackSchema().dump(feedback))

@bp.route("/manga/reports", methods=["GET"])
@moderator_required
@inject
def get_manga_reports_route(
    current_profile,
    report_service: ReportService = Provide[AppContainer.report_container.report_service]
):
    resolved_str = request.args.get("resolved")

    resolved = None
    if resolved_str == "true":
        resolved = True
    elif resolved_str == "false":
        resolved = False 
    
    reports = report_service.user_get_all_manga_reports(current_profile, resolved)

    return respond(data=AdminMangaReportSchema().dump(reports, many=True))


@bp.route("/manga/reports/<int:report_id>", methods=["DELETE"])
@moderator_required
@inject
def resolve_manga_report_route(
    current_profile,
    report_id,
    report_service: ReportService = Provide[AppContainer.report_container.report_service]
):
    report = report_service.user_get_manga_report_by_id(report_id)

    updated_report = report_service.user_resolve_manga_report(current_profile, report)

    return respond(data=AdminMangaReportSchema().dump(updated_report))

@bp.route("/chapters/reports", methods=["GET"])
@moderator_required
@inject
def get_chapters_reports_route(
    current_profile,
    report_service: ReportService = Provide[AppContainer.report_container.report_service]
):
    resolved_str = request.args.get("resolved")

    resolved = None
    if resolved_str == "true":
        resolved = True
    elif resolved_str == "false":
        resolved = False 
    
    reports = report_service.user_get_all_chapters_reports(current_profile, resolved)

    return respond(data=AdminChapterReportSchema().dump(reports, many=True))


@bp.route("/chapters/reports/<int:report_id>", methods=["DELETE"])
@moderator_required
@inject
def resolve_chapter_report_route(
current_profile,
    report_id,
    report_service: ReportService = Provide[AppContainer.report_container.report_service]
):
    report = report_service.user_get_chapter_report_by_id(report_id)

    updated_report = report_service.user_resolve_chapter_report(current_profile, report)

    return respond(data=AdminChapterReportSchema().dump(updated_report))