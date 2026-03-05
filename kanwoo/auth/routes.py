from flask import request, Blueprint
from flask_jwt_extended import (
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)
from marshmallow import ValidationError
from dependency_injector.wiring import inject, Provide

from kanwoo import limiter
from kanwoo import AppContainer
from kanwoo.exceptions import ApiBadRequest, ApiNotFound
from kanwoo.middleware import login_required
from kanwoo.user.exceptions import UserNotFoundException
from kanwoo.user.services import UserService
from kanwoo.user.utils import get_current_user
from kanwoo.utils import respond

from .exceptions import AuthEmailAlreadyTakenException, \
    AuthPasswordNotMatchException, AuthUserWithLoginNotExistException, AuthJWTTokenExpiredException, \
    AuthUserWithEmailNotExistException
from .schemas import AuthRegisterSchema, AuthRecoverySchema
from .services import AuthService, generate_auth_tokens


bp = Blueprint('auth', __name__, url_prefix='/auth')

def generate_tokens_response(access_token: str, refresh_token: str):
    response = respond(data={
        'access_token': access_token,
        'refresh_token': refresh_token,
    })

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@bp.route('/login', methods=['POST'])
@limiter.limit('5 per minute')
@inject
def login_route(
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service]
):
    """ Login user. """
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        access_token, refresh_token = auth_service.login_user(email, password)

        return generate_tokens_response(access_token, refresh_token)
    except AuthPasswordNotMatchException:
        raise ApiBadRequest(detail={"password": ["Invalid password"]})
    except AuthUserWithLoginNotExistException:
        raise ApiBadRequest(detail={"email": ["Invalid email"]})


@bp.route('/register', methods=['POST'])
@limiter.limit('3 per minute')
@inject
def register_route(
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service]
):
    """" Register new user. """
    register_schema = AuthRegisterSchema()

    try:
        data = register_schema.load({
            "email": request.json.get('email'),
            "password": request.json.get('password')
        })

        auth_service.register_user(email=data['email'], password=data['password'])

        return respond(data={
            "success": True,
        }, status_code=201)
    except ValidationError as e:
        raise ApiBadRequest(detail=e.messages)
    except AuthEmailAlreadyTakenException as e:
        raise ApiBadRequest(detail={"email": ["Email already taken"]})


@bp.route('/verify', methods=['GET'])
@limiter.limit('5 per minute')
@login_required
def get_verification_message_route(
    user_service: UserService = Provide[AppContainer.user_container.user_service],
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service]
):
    """ Get user account verification message. """
    user_id = get_current_user()

    try:
        user = user_service.get_by_id(user_id)

        auth_service.send_verification_email(user)

        return respond(data={
            "success": True,
        })
    except UserNotFoundException:
        raise ApiNotFound(detail={"user": ["User not found"]})

@bp.route('/verify', methods=['POST'])
@limiter.limit('3 per minute')
def verify_registration_route(
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service]
):
    token = request.json.get('token')

    if token is None:
        raise ApiBadRequest(detail={"token": ["Token is required"]})

    try:
        access_token, refresh_token = auth_service.verify_user_registration(token)

        return generate_tokens_response(access_token, refresh_token)
    except AuthJWTTokenExpiredException:
        raise ApiBadRequest(detail={"token": ["Token expired"]})


@bp.route('/forgot', methods=['POST'])
@limiter.limit('5 per minute')
def forgot_password_route(
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service]
):
    email = request.json.get('email')

    try:
        auth_service.send_recovery_message(email)

        return respond(data={"success": True})
    except AuthUserWithEmailNotExistException:
        raise ApiBadRequest(detail={"email": ["Invalid email"]})


@bp.route("/recovery", methods=['POST'])
@limiter.limit('5 per minute')
def recovery_password_route(
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service]
):
    recovery_schema = AuthRecoverySchema()

    data = recovery_schema.load({
        "token": request.json.get('token'),
        "password": request.json.get('password'),
    })

    try:
        auth_service.recovery_password(data["token"], data["password"])

        return respond(data={'success': True})
    except AuthPasswordNotMatchException:
        raise ApiBadRequest(detail={"password": ["Invalid password"]})
    except AuthJWTTokenExpiredException:
        raise ApiBadRequest(detail={"token": ["Token expired"]})


@bp.route("/refresh", methods=['POST'])
@limiter.limit('20 per minute')
@login_required(refresh=True) # instead of login_required
def refresh_route(user):
    try:
        access_token, refresh_token = generate_auth_tokens(user)

        return generate_tokens_response(access_token, refresh_token)
    except UserNotFoundException:
        raise ApiNotFound(detail={"user": ["User not found"]})
    
@bp.route("/logout", methods=["POST"])
def logout_route():
    response = respond(data={"success": True})

    unset_jwt_cookies(response)

    return response