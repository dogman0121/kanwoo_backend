from flask import Blueprint, request
from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.middleware import pagination
from kanwoo.profile.middleware import profile_required

from .services import NotificationService
from .schemas import NotificationSchema, NotificationDeleteSchema, NotificationDeleteModeEnum

bp = Blueprint('notifications', __name__, url_prefix='/notifications')


@bp.get("", strict_slashes=False)
@profile_required()
@pagination
@inject
def get_notifications_route(
    current_profile,
    notifications_service: NotificationService = Provide[AppContainer.notification_container.notification_service],
    per_page=20,
    page=1
):
    notifications, notifications_count = notifications_service.user_get_notifications(current_profile, page, per_page)

    return respond(
        data=NotificationSchema().dump(notifications, many=True), 
        total_count=notifications_count, 
        page=page, 
        per_page=per_page
    )

@bp.delete("", strict_slashes=False)
@profile_required()
@inject
def delete_notifications_route(
    current_profile,
    notifications_service: NotificationService = Provide[AppContainer.notification_container.notification_service],
):

    delete_schema = NotificationDeleteSchema().load(request.json)

    notifications_service.user_delete_notificataions(
        current_profile, 
        mode=delete_schema.get("mode"), 
        notifications_ids=delete_schema.get("notifications")
    )

    return respond(data={"success": True})

@bp.post("/read")
def read_notification_route():
    pass