from flask import Blueprint

bp = Blueprint('translation', __name__)

@bp.route('', methods=['GET'], strict_slashes=False)
def get_translations():
    pass

@bp.route('', methods=['POST'], strict_slashes=False)
def post_translation():
    pass

@bp.route('/<int:translation_id>', methods=['GET'])
def get_translation(translation_id):
    pass

@bp.route('/<int:translation_id>', methods=['DELETE'])
def delete_translation(translation_id):
    pass

@bp.route('/<int:translation_id>/chapters', methods=['GET'])
def get_translation_chapters(translation_id):
    pass

@bp.route('/<int:translation_id>/chapters', methods=['POST'])
def post_translation_chapters(translation_id):
    pass

@bp.route('/<int:translation_id>/chapters/<int:chapter_id>', methods=['GET'])
def get_translation_chapter(translation_id, chapter_id):
    pass

@bp.route('/<int:translation_id>/chapters/<int:chapter_id>', methods=['PUT'])
def put_translation_chapter(translation_id, chapter_id):
    pass

@bp.route('/<int:translation_id>/chapters/<int:chapter_id>', methods=['DELETE'])
def delete_translation_chapter(translation_id, chapter_id):
    pass