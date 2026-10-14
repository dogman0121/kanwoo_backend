from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo.middleware import pagination
from kanwoo import AppContainer
from kanwoo.logs import log_runtime
from kanwoo.utils import respond
from kanwoo.entity import FileAction
from kanwoo.profile.middleware import profile_required
from kanwoo.report.dto import ReportCreateDTO
from kanwoo.report.schemas import ReportCreateSchema
from kanwoo.report.services import ReportService
from kanwoo.translation.services import TranslationService
from kanwoo.translation.dto import TranslationCreateDTO
from kanwoo.translation.schemas import GetTranslationSchemaFull, GetTranslationContextSchema
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.moderation.services import ModerationService
from kanwoo.comment.services import CommentService

from .permissions import MangaPolicy
from .schemas import (
    GetMangaSchemaFull,
    GetMangaPermissionSchema, 
    MangaUpdateSchema, 
    MangaEditFormDataSchema,
    MangaSuggestionCreateSchema,
    MangaSuggestionSchema,
    MangaTranslationCreateSchema
)
from .exceptions import MangaNotFoundException
from .services import MangaService, MangaSuggestionService
from .dto import MangaUpdateDTO, NameTranslationDTO, MangaSuggestionCreateDTO

from .handlers import (
    get_manga_list_handler
)

bp = Blueprint('manga', __name__, url_prefix='/manga')

bp.add_url_rule("", methods=["GET"], strict_slashes=False, view_func=get_manga_list_handler)


@bp.route('/<manga_slug>', methods=['GET'])
@log_runtime
@profile_required(optional=True)
@inject
def get_manga_route(
    current_profile, 
    manga_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug, by_link=True)

    return respond(data=GetMangaSchemaFull().dump(manga), status_code=200)

@bp.route("/<manga_slug>", methods=["DELETE"])
@profile_required()
@inject
def delete_manga_route(
    current_profile, 
    manga_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug, by_link=True)

    manga_service.user_delete_manga(current_profile, manga)

    return respond(data={"success": True})

@bp.route("/<manga_slug>/permissions", methods=["GET"])
@profile_required(optional=True)
@inject
def get_manga_permissions_route(
    current_profile, 
    manga_slug,
    manga_policy: MangaPolicy = Provide[AppContainer.manga_container.manga_policy],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    permission_schema = GetMangaPermissionSchema()

    return respond(data=permission_schema.load({
        "edit": manga_policy.can_edit(current_profile, manga),
        "view": manga_policy.can_view(current_profile, manga)
    }))


@bp.route("/<manga_slug>/reports", methods=["POST"])
@profile_required(optional=True)
@inject
def create_report_route(
    current_profile,
    manga_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
    report_service: ReportService = Provide[AppContainer.report_container.report_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug) 
    
    report_data = ReportCreateSchema().load(request.json)

    report_dto = ReportCreateDTO(
        type_id=report_data.get("type"),
        comment=report_data.get("comment")
    )

    report_service.user_create_manga_report(current_profile, manga, report_dto)

    return respond(data={"success": True})

@bp.route("/suggestions", methods=["POST"])
@profile_required(optional=True)
@inject
def suggest_manga_route(
    current_profile,
    manga_suggestion_service: MangaSuggestionService = Provide[AppContainer.manga_container.manga_suggestion_service]
):
    create_data = MangaSuggestionCreateSchema().load(request.json)

    create_dto = MangaSuggestionCreateDTO(
        name=create_data.get("name"),
        comment=create_data.get("message"),
        link=create_data.get("link"),
        creator_id=current_profile.id if current_profile else None
    )

    suggestion = manga_suggestion_service.user_create_suggestion(current_profile, create_dto)

    return respond(data=MangaSuggestionSchema().dump(suggestion))

@bp.route("/check_slug", methods=["GET"])
@inject
def check_slug_route(
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    slug = request.args.get("slug")

    try:
        manga_service.system_get_manga_by_slug(slug)

        return respond(data={"available": False})
    except MangaNotFoundException:
        return respond(data={"available": True})

@bp.get("/<manga_slug>/translations")
@profile_required(optional=True)
@inject
def get_manga_translations_route(
    current_profile, 
    manga_slug,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    official = request.args.get("official", type=bool)

    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    translations = translation_service.user_get_manga_translations(current_profile, manga, official)

    translations_contexts = [
        translation_service.user_get_translation_context(current_profile, translation) 
        for translation in translations
    ]

    return respond(
        data=GetTranslationSchemaFull().dump(translations, many=True),
        context=GetTranslationContextSchema().dump(translations_contexts, many=True)
    )

@bp.route("/<manga_slug>/translations", methods=["POST"])
@profile_required()
@inject
def create_manga_translation_route(
    current_profile, 
    manga_slug,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    create_data = MangaTranslationCreateSchema().load(request.json)

    create_dto = TranslationCreateDTO(
        name=create_data.get("name"),
        lang_id=1, # русский
        privacy_id=create_data.get("privacy"),
        is_official=create_data.get("is_official")
    )

    translation = translation_service.user_create_manga_translation(current_profile, manga, create_dto)

    return respond(data=GetTranslationSchemaFull().dump(translation))
    

@bp.delete("/<manga_slug>/progress")
@profile_required()
@inject
def delete_manga_progress_route(
    current_profile, 
    manga_slug,
    reading_progress_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    reading_progress_service.user_delete_manga_reading_progress(current_profile, manga)

    return respond(data={"success": True})

@bp.post("/<manga_slug>/views")
@profile_required(optional=True)
@inject
def add_view_route(
    current_profile,
    manga_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug, by_link=True)

    manga_service.user_add_manga_view(manga, current_profile)

    return "", 204