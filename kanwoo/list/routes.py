from flask_jwt_extended import jwt_required

from . import bp
from kanwoo import db
from kanwoo.list.schemas import CreateListSchema, ListSchema
from kanwoo.list.models import List, ListVisibility
from kanwoo.list.services import ListService
from kanwoo.user.utils import get_current_user
from kanwoo.utils import respond
from kanwoo.middleware import profile_required

from flask import request

@bp.route('', methods=['GET'], strict_slashes=False)
@profile_required()
def get_lists_route(profile):
    raise NotImplementedError


@bp.route('', methods=['POST'], strict_slashes=False)
@profile_required
def crete_list_route(profile):
    name = request.form.get('name')
    description = request.form.get('description')
    form_visibility = request.form.get('visibility')

    schema = CreateListSchema()

    data = schema.load({
        "name": name,
        "description": description,
        "visibility": form_visibility
    })

    list = ListService(profile).create_list(
        name=data.get("name"), 
        description=data.get("description"), 
        visibility=data.get("visibility", ListVisibility.PRIVATE)
    )

    list_schema = ListSchema()

    return respond(data=list_schema.dump(list))

@bp.route('/<int:list_id>', methods=['PUT'])
@profile_required()
def update_list_route(profile, list_id):
    name = request.form.get('name')
    description = request.form.get('description')

    lst = ListService.get_list(list_id=list_id)
    if profile.id != lst.creator_id:
        return respond(error="forbidden"), 403

    lst.name = name or lst.name
    lst.description = description or lst.description
    db.session.commit()
    return respond(data=lst.to_dict(with_creator=True, with_manga=True)), 200

@bp.route('/<int:list_id>', methods=['GET'])
@profile_required(optional=True)
def get_list_route(user, list_id):
    lst = ListService(user).get_list(list_id)

    schema = ListSchema()

    return respond(data=schema.dump(lst))

@bp.route('/<int:list_id>', methods=['DELETE'])
@profile_required()
def delete_list_route(list_id):
    current_user = get_current_user()
    lst = ListService.get_list(list_id=list_id)
    if current_user.id != lst.creator_id:
        return respond(error="forbidden"), 403

    db.session.delete(lst)
    db.session.commit()

@bp.route('/<int:list_id>/save', methods=['DELETE'])
@profile_required()
def delete_save_route(list_id):
    current_user = get_current_user()
    lst = ListService.get_list(list_id=list_id)

    if lst is None:
        return respond(error="not found"), 404

    lst.remove_save(current_user)
    db.session.commit()

    return {}, 200

@bp.route('/<int:list_id>/save', methods=['POST'])
@profile_required()
def create_save_route(list_id):
    current_user = get_current_user()
    lst = ListService.get_list(list_id=list_id)

    if lst is None:
        return respond(error="not found"), 404

    lst.add_save(current_user)
    db.session.commit()

    return {}, 200

@bp.route('/<int:list_id>/manga', methods=['PUT'])
@profile_required()
def create_manga_route(list_id):
    lst = ListService.get_list(list_id)

    if lst is None:
        return respond(error="not_found"), 404

    manga_id = request.json.get('manga', None)
    if manga_id is None:
        return respond(error="bad_request", detail={"manga": "Titles is empty"}), 400

    manga = MangaService.get_manga(manga_id=manga_id)
    if manga is None:
        return respond(error="not_found"), 404
    lst.add_manga(manga)

    db.session.commit()
    return {}, 200

@bp.route('/<int:list_id>/manga', methods=['DELETE'])
@profile_required()
def delete_manga_route(list_id):
    lst = ListService.get_list(list_id)

    if lst is None:
        return respond(error="not_found"), 404

    manga_id = request.json.get('manga', None)
    if manga_id is None:
        return respond(error="bad_request", detail={"titles": "Titles is empty"}), 400

    manga = MangaService.get_manga(manga_id=manga_id)
    if manga is None:
        return respond(error="not_found"), 404
    lst.remove_manga(manga)

    db.session.commit()

    return {}, 200