from flask import Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo.utils import respond
from kanwoo.containers import AppContainer
from kanwoo.auth.middleware import login_required

from .schemas import SettingsSecuritySchema
from .services import SettingsService

bp = Blueprint("settings", __name__)

@bp.route("/security", methods=["GET"])
@login_required()
@inject
def get_security_settings_route(
    current_user,
    settings_service: SettingsService = Provide[AppContainer.settings_container.settings_service]
):
    security_settings = settings_service.user_get_security_settings(current_user)

    return respond(data=SettingsSecuritySchema().dump(security_settings))

@bp.route("/notifications", methods=["GET"])
def get_notifications_settings_route():
    pass