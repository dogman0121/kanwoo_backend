from flask import request
from marshmallow import ValidationError

from . import bp
from .exceptions import TeamNotFoundException
from .schemas import TeamCreateSchema, TeamSchema
from .services import TeamService
from .dto import TeamCreateDTO

from app.entity import to_file
from app.auth import login_required
from app.exceptions import ApiBadRequest, ApiNotFound
from app.utils import respond


@bp.route('', methods=['GET'], strict_slashes=False)
def index():
    raise NotImplementedError

@bp.route('', methods=['POST'], strict_slashes=False)
@login_required()
def add_team_route(user):
    try:
        create_schema = TeamCreateSchema()

        create_data = create_schema.load(request.form)

        poster = request.files.get('poster')
        if poster:
            poster_file = to_file(poster_file)
        else:
            poster_file = None

        team_create_dto = TeamCreateDTO(
            name=create_data.get("name"),
            about=create_data.get("about"),
            poster=poster_file
        )

        team = TeamService(user).create_team(team_create_dto)

        team_schema = TeamSchema()

        return respond(data = team_schema.dump(team))
    except ValidationError as e:
        raise ApiBadRequest(detail=e.messages)

@bp.route('/<slug>', methods=['GET'], strict_slashes=False)
def get_team(slug):
    try:
        team = TeamService.get_team_by_slug(slug)

        team_schema = TeamSchema()

        raise respond(data = team_schema.dump(team))
    except TeamNotFoundException:
        raise ApiNotFound()

@bp.route('/<slug>', methods=['PUT'], strict_slashes=False)
@login_required()
def update_team(slug):
    raise NotImplementedError

@bp.route('/<slug>/permissions', methods=['GET'], strict_slashes=False)
def get_team_permissions(slug):
    raise NotImplementedError

@bp.route('/<slug>/permissions', methods=['PUT'], strict_slashes=False)
def update_permissions(slug):
    raise NotImplementedError

@bp.route('/<slug>/members', methods=['PATCH'], strict_slashes=False)
def update_members(slug):
    raise NotImplementedError
