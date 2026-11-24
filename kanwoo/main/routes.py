from typing import TYPE_CHECKING
from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from .dto import FeedbackCreateDTO
from .schemas import FeedbackCreateSchema, MetaSchema
from .services import FeedbackService, MetaService
from .handlers import (
    get_upload_urls_handler,
    get_meta_handler
)

bp = Blueprint("main", __name__)

bp.add_url_rule("/meta", view_func=get_meta_handler)
bp.add_url_rule("/uploads", view_func=get_upload_urls_handler)

@bp.route("/feedbacks", methods=["POST"])
@profile_required(optional=True)
@inject
def create_feedback_route(
    current_profile,
    feedback_service: FeedbackService = Provide[AppContainer.main_container.feedback_service]
):
    feedback_data = FeedbackCreateSchema().load(request.json)

    feedback_dto = FeedbackCreateDTO(
        message=feedback_data.get("message")
    )

    feedback_service.user_create_feedback(current_profile, feedback_dto)

    return respond(data={"success": True})