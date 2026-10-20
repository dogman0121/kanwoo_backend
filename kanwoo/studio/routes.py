from flask import Blueprint

from .handlers import (
    get_profile_translations_list_handler,
    get_profile_manga_list_handler,
    get_profile_handler,
    update_profile_handler,
    get_manga_handler,
    update_manga_handler,
    get_manga_edit_form_handler,
    get_manga_translations_handler,
    create_manga_handler,
    create_profile_translation_handler,
    get_translation_handler,
    update_translation_handler,
    get_translations_chapters_handler,
    create_chapter_handler,
    get_chapter_handler,
    update_chapter_handler,
    create_manga_translation_handler
)

bp = Blueprint('studio', __name__, url_prefix='/studio')

bp.add_url_rule("/profiles/<profile_slug>", view_func=get_profile_handler, methods=["GET"])
bp.add_url_rule("/profiles/<profile_slug>", view_func=update_profile_handler, methods=["PUT"])
bp.add_url_rule("/profiles/<profile_slug>/manga", view_func=get_profile_manga_list_handler, methods=["GET"])
bp.add_url_rule("/profiles/<profile_slug>/manga", view_func=create_manga_handler, methods=["POST"])
bp.add_url_rule("/profiles/<profile_slug>/translations", view_func=get_profile_translations_list_handler, methods=["GET"])
bp.add_url_rule("/profiles/<profile_slug>/translations", view_func=create_profile_translation_handler, methods=["POST"])
bp.add_url_rule("/manga/<manga_slug>", view_func=get_manga_handler, methods=["GET"])
bp.add_url_rule("/manga/<manga_slug>", view_func=update_manga_handler, methods=["PUT"])
bp.add_url_rule("/manga/<manga_slug>/forms/info", view_func=get_manga_edit_form_handler, methods=["GET"])
bp.add_url_rule("/manga/<manga_slug>/translations", view_func=get_manga_translations_handler, methods=["GET"])
bp.add_url_rule("/manga/<manga_slug>/translations", view_func=create_manga_translation_handler, methods=["POST"])
bp.add_url_rule("/translations/<int:translation_id>", view_func=get_translation_handler, methods=["GET"])
bp.add_url_rule("/translations/<int:translation_id>", view_func=update_translation_handler, methods=["PUT"])
bp.add_url_rule("/translations/<int:translation_id>/chapters", view_func=get_translations_chapters_handler, methods=["GET"])
bp.add_url_rule("/translations/<int:translation_id>/chapters", view_func=create_chapter_handler, methods=["POST"])
bp.add_url_rule("/chapters/<int:chapter_id>", view_func=get_chapter_handler, methods=["GET"])
bp.add_url_rule("/chapters/<int:chapter_id>", view_func=update_chapter_handler, methods=["PUT"])






