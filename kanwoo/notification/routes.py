from flask import Blueprint

from .services import NotificationService

bp = Blueprint('notifications', __name__, url_prefix='/notifications')


@bp.get("", strict_slashes=False)
def get_notifications_route():
    pass