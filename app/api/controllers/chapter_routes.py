from flask import Blueprint

bp = Blueprint('chapter', __name__)

@bp.route('', methods=['GET'], strict_slashes=False)
def get_chapters():
    pass

@bp.route('', methods=['POST'], strict_slashes=False)
def post_chapters():
    pass

@bp.route('/<int:chapter_id>', methods=['GET'])
def get_chapter(chapter_id):
    pass

@bp.route('/<int:chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    pass

@bp.route('/<int:chapter_id>', methods=['PUT'])
def put_chapter(chapter_id):
    pass