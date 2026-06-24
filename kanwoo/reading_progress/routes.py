from typing import TYPE_CHECKING
from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from .services import ReadingProgressService
from .schemas import ReadingProgressSchema

bp = Blueprint("progress", __name__)


@bp.route("", methods=["GET"], strict_slashes=False)
@profile_required()
@inject
def get_progress_route(
    current_profile,
    reading_progress_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service]
):
    progresses = reading_progress_service.user_get_profile_progresses(current_profile)
    for p in progresses:
        print(p.chapters_count)
    return respond(data=ReadingProgressSchema().dump(progresses, many=True))


@bp.route("/<int:progress_id>", methods=["DELETE"], strict_slashes=False)
@profile_required()
@inject
def delete_progress_route(
    current_profile,
    progress_id,
    reading_progress_service: ReadingProgressService = Provide[AppContainer.reading_progress_container.reading_progress_service]
):
    progress = reading_progress_service.user_get_progress_by_id(current_profile, progress_id)

    reading_progress_service.user_delete_progress(current_profile, progress)

    return respond(data={"success": True})