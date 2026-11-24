from flask import Blueprint

from .handlers import (
    get_history_list_handler,
    delete_history_handler,
    get_bookmarks_list_handler,
    get_bookmark_handler,
    delete_bookmark_handler,
    get_manga_bookmark_handler,
    get_chapter_progress_handler,
    get_reading_session_handler,
    patch_reading_session_handler,
    get_manga_reading_start_handler
)

bp = Blueprint("progress", __name__)

bp.add_url_rule("/history", methods=["GET"], view_func=get_history_list_handler)
bp.add_url_rule("/history", methods=["DELETE"], view_func=delete_history_handler)
bp.add_url_rule("/bookmarks", methods=["GET"], view_func=get_bookmarks_list_handler)
bp.add_url_rule("/bookmarks/<int:bookmark_id>", methods=["GET"], view_func=get_bookmark_handler)
bp.add_url_rule("/bookmarks/<int:bookmark_id>", methods=["DELETE"], view_func=delete_bookmark_handler)
bp.add_url_rule("/bookmarks/manga/<manga_slug>", methods=["GET"], view_func=get_manga_bookmark_handler)
bp.add_url_rule("/reading-sessions", methods=["GET"], view_func=get_reading_session_handler)
bp.add_url_rule("/reading-sessions/<int:session_id>", methods=["PATCH"], view_func=patch_reading_session_handler)
bp.add_url_rule("/chapters/<int:chapter_id>", view_func=get_chapter_progress_handler, methods=["GET"])
bp.add_url_rule("/manga/<manga_slug>/reading-start", view_func=get_manga_reading_start_handler, methods=["GET"])