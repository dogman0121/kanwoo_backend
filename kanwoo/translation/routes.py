from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.middleware import profile_required
from kanwoo.chapter.services import ChapterService
from kanwoo.chapter.dto import ChapterCreateDTO
from kanwoo.chapter.schemas import ChapterCreateSchema, ChapterSchemaFull

from .dto import TranslationUpdateDTO
from .services import TranslationService
from .schemas import TranslationPermissionSchema, TranslationUpdateSchema, TranslationSchemaFull
from .permissions import TranslationPolicy

bp = Blueprint('translation', __name__, url_prefix='/translations')

@bp.route("/<int:translation_id>", methods=["GET"])
@profile_required(optional=True)
def get_translation_route(
    current_profile,
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    return respond(data=TranslationSchemaFull().dump(translation))

@bp.route("/<int:translation_id>", methods=["PUT"])
@profile_required()
@inject
def update_translation_route(
    current_profile, 
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    update_data = TranslationUpdateSchema().load(request.form)

    update_dto = TranslationUpdateDTO(
        name=update_data.get("name"),
        privacy=update_data.get("privacy")
    )

    updated_translation = translation_service.user_update_translation(current_profile, translation, update_dto)

    return respond(data=TranslationSchemaFull().dump(updated_translation))

@bp.route("/<int:translation_id>", methods=["DELETE"])
@profile_required()
@inject
def delete_translation_route(
    current_profile, 
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    translation_service.user_delete_translation(current_profile, translation)

    return respond(data={"sucess": True})

@bp.route("/<int:translation_id>/permissions", methods=["GET"])
@profile_required(optional=True)
def get_translation_permissions_route(
    current_profile, 
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
    translation_policy: TranslationPolicy = Provide[AppContainer.translation_container.translation_policy]
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    permission_schema = TranslationPermissionSchema()

    return respond(data=permission_schema.dump({"edit": translation_policy.can_edit(current_profile, translation)}))

@bp.route("/<int:translation_id>/chapters", methods=["POST"])
@profile_required()
@inject
def create_translation_chapter_route(
    current_profile, 
    translation_id,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    create_data = ChapterCreateSchema().load({
        "name": request.form.get("name"),
        "chapter": request.form.get("chapter"),
        "privacy": request.form.get("privacy"),
        "pages_order": request.form.get("pages_order"),
        "pages": request.files.getlist("pages")
    })

    create_dto = ChapterCreateDTO(
        name = create_data.get("name"),
        chapter = create_data.get("chapter"),
        pages = create_data.get("pages"),
        pages_order = create_data.get("pages_order"),
        privacy=create_data.get("privacy")
    )

    chapter = chapter_service.user_create_translation_chapter(current_profile, translation, create_dto)

    return respond(data=ChapterSchemaFull().dump(chapter))


@bp.route("/<int:translation_id>/chapters", methods=["GET"])
@profile_required(optional=True)
@inject
def get_translation_chapters_route(
    current_profile, 
    translation_id,
    chapter_service: ChapterService = Provide[AppContainer.chapter_container.chapter_service],
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    chapters = chapter_service.user_get_translation_chapters(current_profile, translation)

    return respond(data=ChapterSchemaFull().dump(chapters, many=True))
