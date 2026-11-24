from flask import Blueprint

from .handlers import (
    get_home_handler,
    get_home_block_handler,
    get_home_blocks_list_handler
)

bp = Blueprint('home', __name__, url_prefix='/home')

bp.add_url_rule("", view_func=get_home_handler, methods=['GET'], strict_slashes=False)
bp.add_url_rule("/blocks/<hash>", view_func=get_home_block_handler, methods=['GET'])
bp.add_url_rule("/blocks", view_func=get_home_blocks_list_handler, methods=['POST'])