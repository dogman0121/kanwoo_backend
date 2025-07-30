from flask import Blueprint

bp = Blueprint('list', __name__)

@bp.route('', methods=['GET'], strict_slashes=False)
def get_lists():
    pass

@bp.route('', methods=['POST'], strict_slashes=False)
def post_list():
    pass

@bp.route('/<int:list_id>', methods=['GET'])
def get_list(list_id):
    pass

@bp.route('/<int:list_id>', methods=['PUT'])
def put_list(list_id):
    pass

@bp.route('/<int:list_id>', methods=['DELETE'])
def delete_list(list_id):
    pass

@bp.route('/<int:list_id>/save', methods=['PATCH'])
def patch_list(list_id):
    pass