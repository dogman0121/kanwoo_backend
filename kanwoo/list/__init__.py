from flask import Blueprint

bp = Blueprint('lists', __name__, url_prefix='/lists')

from .routes import (
    delete_list_route,
    delete_manga_route,
    delete_save_route,
    create_manga_route,
    create_save_route,
    crete_list_route,
    get_list_route,
    get_current_user,
    update_list_route
)