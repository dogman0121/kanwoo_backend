from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.chapter.services import ChapterService
from kanwoo.chapter.schemas import GetChapterSchemaFull
from kanwoo.manga.services import MangaService

from .services import TranslationService
from .schemas import (
    GetTranslationPermissionSchema, 
)
from .permissions import TranslationPolicy
from .handlers import (
    get_translation_handler,
    get_translations_list_handler
)

bp = Blueprint('translation', __name__, url_prefix='/translations')

bp.add_url_rule("", methods=["GET"], view_func=get_translations_list_handler)
bp.add_url_rule("/<int:translation_id>", methods=["GET"], view_func=get_translation_handler)

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
@inject
def get_translation_permissions_route(
    current_profile, 
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
    translation_policy: TranslationPolicy = Provide[AppContainer.translation_container.translation_policy]
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    permission_schema = GetTranslationPermissionSchema()

    return respond(data=permission_schema.dump({"edit": translation_policy.can_edit(current_profile, translation)}))

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

    return respond(data=GetChapterSchemaFull().dump(chapters, many=True))


@bp.post("/<int:translation_id>/subscriptions")
@profile_required()
@inject
def subscribe_translation(
    current_profile, 
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)

    translation_service.user_subscribe_translation(current_profile, translation)

    return respond(data={"success": True})

@bp.delete("/<int:translation_id>/subscriptions")
@profile_required()
@inject
def unsubscribe_translation(
    current_profile, 
    translation_id,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    translation = translation_service.user_get_translation_by_id(current_profile, translation_id)
    
    translation_service.user_unsubscribe_translation(current_profile, translation)

    return respond(data={"success": True})