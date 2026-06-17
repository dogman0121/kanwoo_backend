from marshmallow.experimental.context import Context
from flask import request, make_response, Blueprint
import os
from datetime import datetime, timedelta
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.logs import log_runtime
from kanwoo.entity import convert_to_file
from kanwoo.auth.middleware import login_required
from kanwoo.exceptions import ApiForbidden
from kanwoo.utils import respond
from kanwoo.manga.dto import MangaCreateDTO
from kanwoo.manga.schemas import MangaSchema, MangaCreateSchema
from kanwoo.manga.services import MangaService
from kanwoo.translation.dto import TranslationCreateDTO
from kanwoo.translation.services import TranslationService
from kanwoo.translation.schemas import TranslationSchemaFull, TranslationCreateSchema
from kanwoo.reading_progress.services import ReadingProgressService
from kanwoo.collection.services import CollectionService, CollectionScope

from .exceptions import ProfileNotFoundException
from .schemas import (
    ProfileCreateSchema, 
    ProfileSchema, 
    ProfileUpdateSchema, 
    AvatarAction, 
    ProfilePermissionsSchema, 
    ProfileReadingProgressSchema,
    CurrentProfileSchema,
    ProfileCollectionSchema
)
from .services import ProfileService, ProfileAuthService
from .dto import ProfileCreateDTO, ProfileUpdateDTO, ProfileLinkDTO
from .permissions import ProfileAuthPolicy, ProfilePolicy
from .utils import set_auth_profile_cookie
from .middleware import profile_required

bp = Blueprint('profiles', __name__, url_prefix='/profiles')

@bp.route('', methods=['GET'], strict_slashes=False)
@login_required()
@inject
def get_user_profiles_route(
    current_user,
    profile_auth_service: ProfileAuthService = Provide[AppContainer.profile_container.profile_auth_service]
):
    profiles = profile_auth_service.user_get_user_profiles(current_user)
    
    return respond(data=ProfileSchema().dump(profiles, many=True))

@bp.route('/current', methods=['GET'])
@profile_required()
def get_current_profile_route(
    current_profile
):
    return respond(data=CurrentProfileSchema().dump(current_profile)) 

@bp.route('/current', methods=['PUT'])
@login_required()
@inject
def select_profile_route(
    current_user,
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
    profile_auth_policy: ProfileAuthPolicy = Provide[AppContainer.profile_container.profile_auth_policy]
):
    profile_id = request.json.get("profile")

    profile = profile_service.user_get_profile_by_id(current_user, profile_id)

    if not profile_auth_policy.can_use(current_user, profile):
        raise ApiForbidden

    response = make_response(respond(data={"success": True}))
    
    set_auth_profile_cookie(response, profile)

    return response


@bp.route('', methods=['POST'], strict_slashes=False)
@login_required()
@inject
def create_profile_route(
    current_user,
    profile_auth_service: ProfileAuthService = Provide[AppContainer.profile_container.profile_auth_service]
):
    name = request.form.get("name")
    slug = request.form.get("slug")
    avatar = request.files.get("avatar")

    create_data = ProfileCreateSchema().load({
        "name": name,
        "slug": slug,
        "avatar": avatar
    })

    profile_create_dto = ProfileCreateDTO(
        slug=slug,
        name=create_data.get("name"),
        about=create_data.get("about"),
        avatar=create_data.get("avatar"),
        owner_id=current_user.id,
        creator_id=None
    )

    profile = profile_auth_service.user_create_profile(current_user, profile_create_dto)

    return respond(data = ProfileSchema().dump(profile))

@bp.route('/<profile_slug>', methods=['GET'], strict_slashes=False)
@profile_required()
@inject
def get_profile_route(
    current_profile,
    profile_slug,
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service]
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    return respond(data = ProfileSchema().dump(profile))

@bp.route('/<profile_slug>', methods=['PUT'], strict_slashes=False)
@profile_required()
@inject
def update_profile_route(
    current_profile, 
    profile_slug,
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service]
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)
    
    name = request.form.get("name")
    slug = request.form.get("slug")
    avatar_action = request.form.get("avatar_action")
    about = request.form.get("about", "")
    links = request.form.get("links")
    avatar = request.files.get("avatar")

    update_data = ProfileUpdateSchema().load({
        "name": name,
        "slug": slug,
        "avatar_action": avatar_action,
        "about": about,
        "links": links,
        "avatar": avatar,
    })

    profile_update_dto = ProfileUpdateDTO(
        name = update_data.get("name"),
        slug = update_data.get("slug"),
        about = update_data.get("about"),
        links = update_data.get("links"),
        avatar_action = update_data.get("avatar_action", AvatarAction.KEEP),
        avatar = update_data.get("avatar")
    )

    profile = profile_service.user_update_profile(current_profile, profile, profile_update_dto)

    profile_schema = ProfileSchema()

    return respond(data=profile_schema.dump(profile))

@bp.route('/<profile_slug>/permissions', methods=['GET'], strict_slashes=False)
@profile_required(optional=True)
@inject
def get_profile_permissions_route(
    current_profile, 
    profile_slug,
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
    profile_policy: ProfilePolicy = Provide[AppContainer.profile_container.profile_policy]
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    permission_schema = ProfilePermissionsSchema()

    return respond(data=permission_schema.dump({
        "edit": profile_policy.can_edit(current_profile, profile)
    }))


@bp.route('/<slug>/permissions', methods=['PUT'])
def update_permissions(slug):
    raise NotImplementedError

@bp.route('/<profile_slug>/manga', methods=["GET"])
@log_runtime
@profile_required(optional=True)
@inject
def get_profile_manga_route(
    current_profile, 
    profile_slug,
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    manga_list = manga_service.user_get_profile_manga(current_profile, profile)

    manga_schema = MangaSchema()

    return respond(data=manga_schema.dump(manga_list, many=True))

@bp.route("/<profile_slug>/manga", methods=["POST"])
@profile_required()
@inject
def create_profile_manga(
    current_profile,
    profile_slug,
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

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
        genres_ids = create_data.get("genres"),
        privacy_id= create_data.get("privacy"),
        poster = create_data.get("poster"),
        background = create_data.get("background"),
    )

    manga = manga_service.user_create_manga(current_profile, create_dto) 

    manga_schema = MangaSchema()

    return respond(data=manga_schema.dump(manga))

@bp.route('/check_slug', methods=["GET"])
@inject
def check_slug_route(
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
):
    slug = request.args.get("slug")

    try:
        profile_service.system_get_profile_by_slug(slug)

        return respond(data={"available": False})
    except ProfileNotFoundException:
        return respond(data={"available": True})

@bp.route("/<profile_slug>/translations", methods=["GET"])
@profile_required(optional=True)
@inject
def get_profile_translations(
    current_profile, 
    profile_slug,
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service],
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    translations = translation_service.user_get_profile_translations(profile)

    return respond(data=TranslationSchemaFull().dump(translations, many=True))


@bp.route("/<profile_slug>/translations", methods=["POST"])
@profile_required()
@inject
def create_profile_translation(
    current_profile,
    profile_slug,
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
    translation_service: TranslationService = Provide[AppContainer.translation_container.translation_service]
):
    create_schema_data = TranslationCreateSchema().load(request.json)

    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    create_dto = TranslationCreateDTO(
        name=create_schema_data["name"],
        privacy_id=create_schema_data["privacy"],
        lang_id=1,
        is_official=False,
    )

    manga = manga_service.user_get_manga_by_id(current_profile, create_schema_data["manga"])

    translation = translation_service.user_create_manga_translation(current_profile, profile, manga, create_dto)

    return respond(data=TranslationSchemaFull().dump(translation))


@bp.route("/<profile_slug>/progress")
@profile_required()
@inject
def get_profile_reading_progress(
    current_profile,
    profile_slug,
    reading_progress_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service],
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service],
):
    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    reading_progresses = reading_progress_service.user_get_profile_progress(current_profile, profile)

    return respond(data=ProfileReadingProgressSchema().dump(reading_progresses, many=True))

@bp.route("/<profile_slug>/collections")
@profile_required()
@inject
def get_profile_collections_route(
    current_profile,
    profile_slug,
    collection_service: CollectionService = Provide[AppContainer.collection_container.collection_service],
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service]
):
    from_manga = request.args.get("from_manga")
    scope = request.args.get("scope", "all")

    if scope == "creator":
        scope_enum = CollectionScope.CREATOR
    else:
        scope_enum = CollectionScope.ALL

    profile = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    collections = collection_service.user_get_profile_collections(
        current_profile, 
        profile, 
        scope=scope_enum, 
    )


    with Context({"manga_slug": from_manga}):
        return respond(data=ProfileCollectionSchema(many=True).dump(collections))

