from flask import request
from marshmallow import ValidationError

from . import bp
from .exceptions import TeamNotFoundException, TeamUpdateNotAllowedException
from .schemas import TeamCreateSchema, TeamSchema, TeamUpdateSchema, AvatarAction
from .services import TeamService
from .dto import TeamCreateDTO, TeamUpdateDTO, TeamLinkDTO

from app.entity import to_file
from app.auth import login_required
from app.exceptions import ApiBadRequest, ApiNotFound, ApiForbidden
from app.utils import respond


@bp.route('', methods=['GET'], strict_slashes=False)
def index():
    raise NotImplementedError

@bp.route('', methods=['POST'], strict_slashes=False)
@login_required()
def add_team_route(user):
    try:
        name = request.form.get("name")
        about = request.form.get("about")

        create_schema = TeamCreateSchema()
        create_data = create_schema.load({
            "name": name,
            "about": about
        })

        avatar = request.files.get('avatar')
        if avatar:
            avatar_file = to_file(avatar)
        else:
            avatar_file = None

        team_create_dto = TeamCreateDTO(
            name=create_data.get("name"),
            about=create_data.get("about"),
            avatar=avatar_file
        )

        team = TeamService(user).create_team(team_create_dto)

        team_schema = TeamSchema()

        return respond(data = team_schema.dump(team))
    except ValidationError as e:
        raise ApiBadRequest(detail=e.messages)

@bp.route('/<slug>', methods=['GET'], strict_slashes=False)
def get_team_route(slug):
    try:
        team = TeamService.get_team_by_slug(slug)

        team_schema = TeamSchema()

        return respond(data = team_schema.dump(team))
    except TeamNotFoundException:
        raise ApiNotFound

@bp.route('/<slug>', methods=['PUT'], strict_slashes=False)
@login_required()
def update_team_route(user, slug):
    try:
        team = TeamService.get_team_by_slug(slug)
        
        name = request.form.get("name")
        slug = request.form.get("slug")
        avatar_action = request.form.get("avatar_action")
        about = request.form.get("about", "")
        links = request.form.get("links")

        update_schema = TeamUpdateSchema()
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

        links = [TeamLinkDTO(name=i["name"], link=i["link"]) for i in update_data.get("links")]

        team_update_dto = TeamUpdateDTO(
            name = update_data.get("name"),
            slug = update_data.get("slug"),
            about = update_data.get("about"),
            links = links,
            avatar_action = update_data.get("avatar_action", AvatarAction.KEEP),
            avatar = avatar_file
        )

        team = TeamService(user).update_team(team, team_update_dto)

        team_schema = TeamSchema()

        return respond(data=team_schema.dump(team))

    except TeamNotFoundException:
        raise ApiNotFound
    except ValidationError as e:
        raise ApiBadRequest(detail=e.messages)
    except TeamUpdateNotAllowedException:
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
        TeamService.get_team_by_slug(slug)

        return respond(data={"available": False})
    except TeamNotFoundException:
        return respond(data={"available": True})

