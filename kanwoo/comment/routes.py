from flask import Blueprint

from .handlers import (
    get_comments_list_handler,
    create_comment_handler,
    get_comment_handler,
    delete_comment_handler,
    get_comment_replies_handler,
    reply_comment_handler,
    vote_comment_handler,
    get_comment_subthreads_handler,
    get_subthread_discussion_handler,
    get_comments_preview_handler
)

bp = Blueprint("comment", __name__)

bp.add_url_rule("", methods=["GET"], view_func=get_comments_list_handler, strict_slashes=False)
bp.add_url_rule("", methods=["POST"], view_func=create_comment_handler, strict_slashes=False)
bp.add_url_rule("/preview", methods=["GET"], view_func=get_comments_preview_handler)
bp.add_url_rule("/<int:comment_id>", methods=["GET"], view_func=get_comment_handler)
bp.add_url_rule("/<int:comment_id>", methods=["DELETE"], view_func=delete_comment_handler)
bp.add_url_rule("/<int:comment_id>/votes", methods=["PATCH"], view_func=vote_comment_handler)
bp.add_url_rule("/<int:comment_id>/replies", methods=["GET"], view_func=get_comment_replies_handler)
bp.add_url_rule("/<int:comment_id>/replies", methods=["POST"], view_func=reply_comment_handler)
bp.add_url_rule("/<int:comment_id>/subthreads", methods=["GET"], view_func=get_comment_subthreads_handler)
bp.add_url_rule("/subthreads/<int:subthread_id>/discussion", methods=["GET"], view_func=get_subthread_discussion_handler)

    
    
# @bp.route("/<int:comment_id>/reports", methods=["POST"])
# @profile_required(optional=True)
# @inject
# def report_comment_route(
#     current_profile,
#     comment_id,
#     comment_service: CommentService = Provide[AppContainer.comment_container.comment_service],
#     report_service: ReportService = Provide[AppContainer.report_container.report_service]

# ):
#     comment = comment_service.user_get_comment_by_id(current_profile, comment_id)

#     create_report_schema = ReportCreateSchema().load(request.json)

#     create_report_dto = ReportCreateDTO(
#         type_id=create_report_schema.get("type"),
#         comment=create_report_schema.get("comment")
#     )

#     report_service.user_create_comment_report(current_profile, comment, create_report_dto)

#     return respond(data={"success": True})