from typing import TYPE_CHECKING
from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from .dto import FeedbackCreateDTO
from .schemas import FeedbackCreateSchema, MetaSchema
from .services import FeedbackService, MetaService

bp = Blueprint("main", __name__)

@bp.route("/meta", methods=["GET"])
@inject
def get_meta_route(
    meta_service: MetaService = Provide[AppContainer.main_container.meta_service]
):
    meta = meta_service.user_get_meta()

    return respond(data=MetaSchema().dump(meta))


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