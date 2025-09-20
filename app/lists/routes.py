from flask_jwt_extended import jwt_required

from . import bp
from app import db
from app.lists.schemas import CreateListSchema, ListSchema
from app.lists.models import List, ListVisibility
from app.lists.services import ListService
from app.user.utils import get_current_user
from app.utils import respond
from app.auth.middleware import login_required

from flask import request

@bp.route('', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_lists():
    current_user = get_current_user()

    return respond(data=[l.to_dict() for l in current_user.lists])


@bp.route('', methods=['POST'], strict_slashes=False)
@login_required
def add_list():
    current_user = get_current_user()

    name = request.form.get('name')
    description = request.form.get('description')
    form_visibility = request.form.get('visibility', ListVisibility.PRIVATE.value)

    if form_visibility == "link":
        visibility = ListVisibility.LINK
    elif form_visibility == "public":
        visibility = ListVisibility.PUBLIC
    elif form_visibility == "private":
        visibility = ListVisibility.PRIVATE
    else:
        visibility = ListVisibility.PRIVATE

    schema = CreateListSchema()

    data = schema.load({
        "name": name,
        "description": description,
        "visibility": visibility
    })

    list = ListService(current_user).create_list(
        name=data["name"], 
        description=data["description"], 
        visibility=data["visibility"]
    )

    list_schema = ListSchema()

    return respond(data=list_schema.dump(list))

@bp.route('/<int:list_id>', methods=['PUT'])
@jwt_required()
def update_list(list_id):
    current_user = get_current_user()
    name = request.form.get('name')
    description = request.form.get('description')

    lst = ListService.get_list(list_id=list_id)
    if current_user.id != lst.creator_id:
        return respond(error="forbidden"), 403

    lst.name = name or lst.name
    lst.description = description or lst.description
    db.session.commit()
    return respond(data=lst.to_dict(with_creator=True, with_manga=True)), 200

@bp.route('/<int:list_id>', methods=['GET'])
def get_list(list_id):
    current_user = get_current_user()

    lst = ListService(current_user).get_list(list_id)

    schema = ListSchema()

    return respond(data=schema.dump(lst))

@bp.route('/<int:list_id>', methods=['DELETE'])
@jwt_required()
def delete_list(list_id):
    current_user = get_current_user()
    lst = ListService.get_list(list_id=list_id)
    if current_user.id != lst.creator_id:
        return respond(error="forbidden"), 403

    db.session.delete(lst)
    db.session.commit()

@bp.route('/<int:list_id>/save', methods=['DELETE'])
@jwt_required()
def delete_save(list_id):
    current_user = get_current_user()
    lst = ListService.get_list(list_id=list_id)

    if lst is None:
        return respond(error="not found"), 404

    lst.remove_save(current_user)
    db.session.commit()

    return {}, 200

@bp.route('/<int:list_id>/save', methods=['POST'])
@jwt_required()
def add_save(list_id):
    current_user = get_current_user()
    lst = ListService.get_list(list_id=list_id)

    if lst is None:
        return respond(error="not found"), 404

    lst.add_save(current_user)
    db.session.commit()

    return {}, 200

@bp.route('/<int:list_id>/manga', methods=['PUT'])
@jwt_required()
def add_manga(list_id):
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
@jwt_required()
def delete_manga(list_id):
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