from flask import Blueprint

from .handlers import (
    get_progresses_handler,
    get_history_handler,
    delete_progress_handler,
    delete_history_handler,
    create_progress_handler,
    update_progress_handler,
    get_manga_progress_handler,
    get_chapter_progress_handler
)

bp = Blueprint("progress", __name__)

bp.add_url_rule("", view_func=get_progresses_handler, strict_slashes=False, methods=["GET"])
bp.add_url_rule("", view_func=create_progress_handler, strict_slashes=False, methods=["POST"])
bp.add_url_rule("/<int:progress_id>", view_func=update_progress_handler, methods=["PATCH"])
bp.add_url_rule("/<int:progress_id>", view_func=delete_progress_handler, methods=["DELETE"])
bp.add_url_rule("/history", view_func=get_history_handler, methods=["GET"])
bp.add_url_rule("/history", view_func=delete_history_handler, methods=["DELETE"])
bp.add_url_rule("/manga/<manga_slug>", view_func=get_manga_progress_handler, methods=["GET"])
bp.add_url_rule("/chapters/<int:chapter_id>", view_func=get_chapter_progress_handler, methods=["GET"])