from flask import request
from marshmallow import ValidationError

from . import bp
from .exceptions import TeamNotFoundException
from .schemas import TeamCreateSchema, TeamSchema
from .services import TeamService

from app.auth import login_required
from app.exceptions import HTTPBadRequest, HTTPNotFound
from app.user.utils import get_current_user
from app.utils import respond


@bp.route('', methods=['GET'], strict_slashes=False)
def index():
    raise NotImplementedError

@bp.route('', methods=['POST'], strict_slashes=False)
@login_required()
def add_team():
    current_user = get_current_user()

    create_schema = TeamCreateSchema()

    try:
        create_data = create_schema.load(request.form)

        team = TeamService(current_user).create_team(create_data, request.files['poster'])

        team_schema = TeamSchema()

        raise respond(data = team_schema.dump(team))
    except ValidationError as e:
        raise HTTPBadRequest(detail=e.messages)

@bp.route('/<slug>', methods=['GET'], strict_slashes=False)
def get_team(slug):
    try:
        team = TeamService.get_team_by_slug(slug)

        team_schema = TeamSchema()

        raise respond(data = team_schema.dump(team))
    except TeamNotFoundException:
        raise HTTPNotFound()

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
