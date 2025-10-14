from flask import request, make_response
from marshmallow import ValidationError

from . import bp
from .exceptions import ProfileNotFoundException, ProfileUpdateNotAllowedException
from .schemas import ProfileCreateSchema, ProfileSchema, ProfileUpdateSchema, AvatarAction
from .services import ProfileService
from .dto import ProfileCreateDTO, ProfileUpdateDTO, ProfileLinkDTO
from .permissions import ProfilePolicy
from .middleware import profile_required

from app.entity import to_file
from app.auth import login_required
from app.exceptions import ApiBadRequest, ApiNotFound, ApiForbidden
from app.utils import respond


@bp.route('', methods=['GET'], strict_slashes=False)
@login_required()
def get_user_profiles_route(user):
    profiles = ProfileService(user).get_profiles()
    
    schema = ProfileSchema()

    return respond(data=schema.dump(profiles, many=True))

@bp.route('/current', methods=['GET'])
@profile_required
def get_current_profile_route(profile):

    schema = ProfileSchema()

    return respond(data=schema.dump(profile)) 

@bp.route('/select', methods=['POST'])
@login_required()
def select_profile_route(user):
    try:
        profile_id = request.json.get("profile_id")

        profile = ProfileService(user).get_profile_by_id(profile_id)

        if not ProfilePolicy(user).can_use(profile):
            raise ApiForbidden

        response = make_response(respond(data={"success": True}))

        response.set_cookie(
            "auth_profile", 
            str(profile_id), 
            path="/",
            domain="localhost",
            secure=True,
            httponly=True,
        )

        return response
    except ProfileNotFoundException:
        raise ApiNotFound


@bp.route('', methods=['POST'], strict_slashes=False)
@login_required()
def add_profile_route(user):
    try:
        name = request.form.get("name")
        about = request.form.get("about", "")

        create_schema = ProfileCreateSchema()
        create_data = create_schema.load({
            "name": name,
            "about": about
        })

        avatar = request.files.get('avatar')
        if avatar:
            avatar_file = to_file(avatar)
        else:
            avatar_file = None

        profile_create_dto = ProfileCreateDTO(
            name=create_data.get("name"),
            about=create_data.get("about"),
            avatar=avatar_file
        )

        profile = ProfileService(user).create_profile(profile_create_dto)

        profile_schema = ProfileSchema()

        return respond(data = profile_schema.dump(profile))
    except ValidationError as e:
        raise ApiBadRequest(detail=e.messages)

@bp.route('/<slug>', methods=['GET'], strict_slashes=False)
def get_profile_route(slug):
    try:
        profile = ProfileService.get_team_by_slug(slug)

        profile_schema = ProfileSchema()

        return respond(data = profile_schema.dump(profile))
    except ProfileNotFoundException:
        raise ApiNotFound

@bp.route('/<slug>', methods=['PUT'], strict_slashes=False)
@login_required()
def update_profile_route(user, slug):
    try:
        profile = ProfileService.get_team_by_slug(slug)
        
        name = request.form.get("name")
        slug = request.form.get("slug")
        avatar_action = request.form.get("avatar_action")
        about = request.form.get("about", "")
        links = request.form.get("links")

        update_schema = ProfileUpdateSchema()
        update_data = update_schema.load({
            "name": name,
            "slug": slug,
            "avatar_action": avatar_action,
            "about": about,
            "links": links
        })

        avatar = request.files.get('avatar')
        if avatar:
            avatar_file = to_file(avatar)
        else:
            avatar_file = None

        links = [ProfileLinkDTO(name=i["name"], link=i["link"]) for i in update_data.get("links")]

        profile_update_dto = ProfileUpdateDTO(
            name = update_data.get("name"),
            slug = update_data.get("slug"),
            about = update_data.get("about"),
            links = links,
            avatar_action = update_data.get("avatar_action", AvatarAction.KEEP),
            avatar = avatar_file
        )

        profile = ProfileService(user).update_profile(profile, profile_update_dto)

        team_schema = ProfileSchema()

        return respond(data=team_schema.dump(profile))

    except ProfileNotFoundException:
        raise ApiNotFound
    except ValidationError as e:
        raise ApiBadRequest(detail=e.messages)
    except ProfileUpdateNotAllowedException:
        raise ApiForbidden

@bp.route('/<slug>/permissions', methods=['GET'], strict_slashes=False)
def get_team_permissions(slug):
    raise NotImplementedError

@bp.route('/<slug>/permissions', methods=['PUT'], strict_slashes=False)
def update_permissions(slug):
    raise NotImplementedError

@bp.route('/<slug>/members', methods=['PATCH'], strict_slashes=False)
def update_members(slug):
    raise NotImplementedError


@bp.route('/check_slug', methods=["GET"])
def check_slug_route():
    slug = request.args.get("slug")

    try:
        ProfileService.get_team_by_slug(slug)

        return respond(data={"available": False})
    except ProfileNotFoundException:
        return respond(data={"available": True})

