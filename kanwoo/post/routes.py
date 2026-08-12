from flask import Blueprint

from .services import PostService

bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.route("", methods=["GET"], strict_slashes=False)
def get_posts_route():
    raise NotImplementedError