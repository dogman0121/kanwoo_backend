from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.logs import log_runtime
from kanwoo.utils import respond
from kanwoo.middleware import profile_required
from kanwoo.entity import FileAction
from kanwoo.report.dto import ReportCreateDTO
from kanwoo.report.schemas import ReportCreateSchema
from kanwoo.report.services import ReportService
from kanwoo.translation.services import TranslationService
from kanwoo.translation.dto import TranslationCreateDTO
from kanwoo.translation.schemas import TranslationCreateSchema, TranslationSchemaFull, TranslationSchemaMini
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.moderation.services import ModerationService

from .permissions import MangaPolicy
from .schemas import (
    MangaSchema, 
    MangaCreateSchema, 
    MangaUpdateSchema, 
    MangaEditFormDataSchema,
    MangaPermissionSchema, 
    ReadingProgressSchema,
    MangaSuggestionCreateSchema,
    MangaSuggestionSchema
)
from .exceptions import MangaNotFoundException
from .services import MangaService, MangaSuggestionService
from .dto import MangaCreateDTO, MangaUpdateDTO, NameTranslationDTO, MangaSuggestionCreateDTO

bp = Blueprint('manga', __name__, url_prefix='/manga')

@bp.route("", methods=["POST"], strict_slashes=False)
@profile_required()
@inject
def create_manga_route(
    current_profile,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
    moderation_service: ModerationService = Provide[AppContainer.moderation_container.moderation_service]
):
    name = request.form.get("name")
    description = request.form.get("description")
    type = request.form.get("type", 0)
    status = request.form.get("status", 0)
    adult = request.form.get("adult", 0)
    genres = request.form.getlist("genre", int)
    year = request.form.get("year")
    background = request.files.get("background")
    poster = request.files.get("poster")

    create_data = MangaCreateSchema().load({
        "name": name,
        "description": description,
        "type": type,
        "status": status,
        "adult": adult,
        "genres": genres,
        "year": year,
        "background": background,
        "poster": poster
    })

    create_dto = MangaCreateDTO(
        name = create_data.get("name"),
        description = create_data.get("description"),
        type_id = create_data.get("type"),
        status_id = create_data.get("status"),
        adult_id = create_data.get("adult"),
        year = create_data.get("year"),
        genres_id = create_data.get("genres"),
        privacy_id= create_data.get("privacy"),
        poster = create_data.get("poster"),
        background = create_data.get("background"),
        author_id=current_profile.id
    )

    manga = manga_service.user_create_manga(current_profile, create_dto) 

    manga_schema = MangaSchema()

    return respond(data=manga_schema.dump(manga))


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

    return respond(data=MangaSchema().dump(manga), status_code=200)


@bp.route("/<manga_slug>", methods=["PUT"])
@profile_required()
@inject
def update_manga_route(
    profile, 
    manga_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(manga_slug, by_link=True)

    new_slug = request.form.get("slug")
    name = request.form.get("name")
    description = request.form.get("description")
    type = request.form.get("type", 0)
    status = request.form.get("status", 0)
    adult = request.form.get("adult", 0)
    genres = request.form.getlist("genre", int)
    year = request.form.get("year")
    name_translations = request.form.get("nameTranslations", "[]")
    background = request.files.get("background")
    poster = request.files.get("poster")
    background_action = request.form.get("backgroundAction", FileAction.KEEP)
    poster_action = request.form.get("posterAction", FileAction.KEEP)
    promo_name = request.files.get("promoName")
    promo_logo = request.files.get("promoLogo")
    promo_background = request.files.get("promoBackground")
    promo_name_action = request.form.get("promoNameAction", FileAction.KEEP)
    promo_logo_action = request.form.get("promoLogoAction", FileAction.KEEP)
    promo_background_action = request.form.get("promoBackgroundAction", FileAction.KEEP)

    update_data = MangaUpdateSchema().load({
        "name": name,
        "slug": new_slug,
        "description": description,
        "type": type,
        "status": status,
        "adult": adult,
        "genres": genres,
        "year": year,
        "name_translations": name_translations,
        "background": background,
        "poster": poster,
        "background_action": background_action,
        "poster_action": poster_action,
        "promo_name": promo_name,
        "promo_logo": promo_logo,
        "promo_background": promo_background,
        "promo_name_action": promo_name_action,
        "promo_logo_action": promo_logo_action,
        "promo_background_action": promo_background_action
    })

    name_translations_prepared = []
    for translation in update_data.get("name_translations"):
        t = NameTranslationDTO(
            lang_id=translation.get("lang"),
            name=translation.get("name")
        )
        name_translations_prepared.append(t)

    update_dto = MangaUpdateDTO(
        name = update_data.get("name"),
        slug = update_data.get("slug"),
        description = update_data.get("description"),
        type_id = update_data.get("type"),
        status_id = update_data.get("status"),
        adult_id = update_data.get("adult"),
        year = update_data.get("year"),
        genres_id = update_data.get("genres"),
        privacy_id= update_data.get("privacy_id"),
        name_translations = name_translations_prepared,
        poster = update_data.get("poster"),
        background = update_data.get("background"),
        poster_action = update_data.get("poster_action"),
        background_action = update_data.get("background_action"),
        promo_name = update_data.get("promo_name"),
        promo_logo = update_data.get("promo_logo"),
        promo_background = update_data.get("promo_background"),
        promo_name_action = update_data.get("promo_name_action"),
        promo_logo_action = update_data.get("promo_logo_action"),
        promo_background_action = update_data.get("promo_background_action")
    )

    updated_manga = manga_service.user_update_manga(profile, manga, update_dto)

    return respond(data=MangaSchema().dump(updated_manga))

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

    permission_schema = MangaPermissionSchema()

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
    
@bp.route("/<manga_slug>/forms/edit", methods=["GET"])
@profile_required()
@inject
def get_manga_form_route(
    current_profile, 
    manga_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    manga_data, blocked_fields = manga_service.user_get_manga_edit_form(current_profile, manga)

    return respond(
        data=MangaEditFormDataSchema().dump(manga_data),
        metadata={"blocked_fields": blocked_fields}
    )

@bp.route("/<manga_slug>/translations", methods=["GET"])
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

    return respond(data=TranslationSchemaMini().dump(translations, many=True))

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

    create_data = TranslationCreateSchema().load(request.json)

    create_dto = TranslationCreateDTO(
        name=create_data.get("name"),
        lang=1, # русский
        privacy=create_data.get("privacy"),
        is_official=create_data.get("is_official")
    )

    translation = translation_service.user_create_manga_translation(current_profile, manga, create_dto)

    return respond(data=TranslationSchemaFull().dump(translation))
    

@bp.route("/<manga_slug>/progress", methods=["GET"])
@profile_required()
@inject
def get_manga_progress_route(
    current_profile, 
    manga_slug,
    reading_progress_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    reading_progress = reading_progress_service.user_get_manga_progress(current_profile, manga)

    return respond(data=ReadingProgressSchema().dump(reading_progress))

@bp.route("/<manga_slug>/progress", methods=["DELETE"])
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
