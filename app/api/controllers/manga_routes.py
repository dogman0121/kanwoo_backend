from flask import Blueprint, request, abort
from marshmallow import ValidationError

from app.api.adapters.manga_form_adapter import MangaFormAdapter
from app.api.middleware import login_required
from app.api.schemas.manga.manga_schema import MangaSchema
from app.api.utils import get_current_user
from app.infrastructure.repositories import SQLMangaRepository
from app.use_cases.manga.create_manga import CreateMangaUseCase
from app.utils import create_response

bp = Blueprint('manga', __name__, url_prefix='/manga')

@bp.route('', methods=['GET'], strict_slashes=False)
def get_mangas():
    pass

@bp.route('', methods=['POST'], strict_slashes=False)
@login_required
def post_manga():
    current_user = get_current_user()

    try:
        data = MangaFormAdapter().adapt(request.form, request.files)
    except ValidationError as e:
        return create_response(error="bad_request", detail=e.messages, status_code=400)

    res = CreateMangaUseCase(SQLMangaRepository()).execute(current_user, data)

    schema = MangaSchema()

    return create_response(data=schema.dump(res), status_code=201)

@bp.route('/<slug>', methods=['GET'])
def get_manga(slug):
    return abort(501)

@bp.route('/<slug>', methods=['PUT'])
def put_manga(slug):
    return abort(501)

@bp.route('/<slug>', methods=['DELETE'])
def delete_manga(slug):
    return abort(501)

@bp.route('/<slug>/permissions', methods=['GET'])
def get_manga_permissions(slug):
    return abort(501)

@bp.route('/<slug>/translations', methods=['GET'])
def get_manga_translations(slug):
    return abort(501)

@bp.route('/<slug>/translations', methods=['POST'])
def post_manga_translations(slug):
    return abort(501)

@bp.route('/<slug>/translations/<int:translation_id>', methods=['GET'])
def get_manga_translation(slug, translation_id):
    return abort(501)

@bp.route('/<slug>/translations/<int:translation_id>', methods=['PUT'])
def put_manga_translation(slug, translation_id):
    return abort(501)

@bp.route('/<slug>/translations/<int:translation_id>', methods=['DELETE'])
def delete_manga_translation(slug, translation_id):
    return abort(501)

@bp.route('/<slug>/translations/<int:translation_id>/chapters', methods=['GET'])
def get_manga_translation_chapters(slug, translation_id):
    return abort(501)

@bp.route('/<slug>/translations/<int:translation_id>/chapters', methods=['POST'])
def post_manga_translation_chapters(slug, translation_id):
    return abort(501)

@bp.route('/<slug>/translations/<int:translation_id>/chapters/<int:chapter_id>', methods=['GET'])
def get_manga_translation_chapter(slug, translation_id, chapter_id):
    return abort(501)