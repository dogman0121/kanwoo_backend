from flask import request, Blueprint
from flask_jwt_extended import (
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)
from marshmallow import ValidationError
from dependency_injector.wiring import inject, Provide

from kanwoo import limiter
from kanwoo import AppContainer
from kanwoo.exceptions import ApiBadRequest, ApiNotFound
from kanwoo.user.exceptions import UserNotFoundException
from kanwoo.utils import respond
from kanwoo.profile.services import ProfileAuthService
from kanwoo.profile.dto import ProfileCreateDTO
from kanwoo.profile.utils import set_auth_profile_cookie
from kanwoo.profile.schemas import CurrentProfileSchema

from .exceptions import AuthEmailAlreadyTakenException, \
    AuthPasswordNotMatchException, AuthUserWithLoginNotExistException, AuthJWTTokenExpiredException
from .schemas import AuthRegisterSchema, AuthRecoverySchema, AuthEmailVerificationCodeSchema, AuthLoginSchema, AuthForgotSchema, AuthYandexOauthSchema
from .services import AuthService, JWTService, YandexOauthService
from .dto import AuthRegisterDTO, AuthRecoveryDTO, AuthLoginDTO, AuthYandexOauthDTO
from .middleware import login_required



bp = Blueprint('auth', __name__, url_prefix='/auth')

def generate_tokens_response(access_token: str, refresh_token: str):
    response = respond(data={
        'access_token': access_token,
        'refresh_token': refresh_token,
    })

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response

def set_tokens_cookie(response, access_token: str, refresh_token: str):
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)


@bp.route('/login', methods=['POST'])
@limiter.limit('5 per minute')
@inject
def login_route(
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service],
    profile_auth_service: ProfileAuthService = Provide[AppContainer.profile_container.profile_auth_service],
    jwt_service: JWTService = Provide[AppContainer.auth_container.jwt_service]
):
    """ Login user. """
    data = AuthLoginSchema().load(request.json)

    login_dto = AuthLoginDTO(
        email=data.get("email"),
        password=data.get("password")
    )

    try:
        user = auth_service.system_login_user(login_dto)

        access_token, refresh_token = jwt_service.create_auth_tokens(user.id)

        profiles = profile_auth_service.user_get_user_profiles(user)

        response = respond(data=CurrentProfileSchema().dump(profiles, many=True))

        set_tokens_cookie(response, access_token, refresh_token)

        return response
    except AuthUserWithLoginNotExistException:
        raise ApiBadRequest(detail={"email": ["Invalid email"]})


@bp.route('/register/code', methods=["GET"])
@inject
def get_verify_registration_code_route(
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service]
):
    data = AuthEmailVerificationCodeSchema().load({
        "email": request.args.get("email")
    })

    auth_service.system_send_email_verification_message(data.get("email"))

    return respond(data={"success": True}), 200


@bp.route('/register', methods=['POST'])
@limiter.limit('10 per minute')
@inject
def register_route(
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service],
    profile_auth_service: ProfileAuthService = Provide[AppContainer.profile_container.profile_auth_service],
    jwt_service: JWTService = Provide[AppContainer.auth_container.jwt_service]
):
    """" Register new user. """
    register_schema = AuthRegisterSchema()

    try:
        data = register_schema.load(request.json)

        register_dto = AuthRegisterDTO(
            code=data.get("code"),
            email=data.get("email"),
            password=data.get("password")
        )
        
        user = auth_service.system_register_user(register_dto)

        profile_dto = ProfileCreateDTO(
            name=data.get("login"),
            slug=data.get("login"),
            about=None,
            avatar=None,
            creator_id=user.id
        )

        profile = profile_auth_service.system_create_profile(profile_dto)

        access_token, refresh_token = jwt_service.create_auth_tokens(user.id)

        response = respond(data=CurrentProfileSchema().dump(profile))

        set_tokens_cookie(response, access_token, refresh_token)

        set_auth_profile_cookie(response, profile)

        return response
    except ValidationError as e:
        raise ApiBadRequest(detail=e.messages)
    except AuthEmailAlreadyTakenException as e:
        raise ApiBadRequest(detail={"email": ["Email already taken"]})


@bp.route("/forgot", methods=["POST"])
@inject
def forgot_password_rotue(
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service]
):
    data = AuthForgotSchema().load(request.json)

    email = data.get("email")

    auth_service.system_send_recovery_message(email)

    return respond(data={"success": True}), 201


@bp.route("/recovery", methods=['POST'])
@limiter.limit('5 per minute')
@inject
def recovery_password_route(
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service]
):
    recovery_schema = AuthRecoverySchema()

    data = recovery_schema.load(request.json)

    recovery_dto = AuthRecoveryDTO(
        token=data.get("token"),
        new_password=data.get("password")
    )

    try:
        auth_service.system_recovery_password(recovery_dto)

        return respond(data={'success': True})
    except AuthPasswordNotMatchException:
        raise ApiBadRequest(detail={"password": ["Invalid password"]})
    except AuthJWTTokenExpiredException:
        raise ApiBadRequest(detail={"token": ["Token expired"]})


@bp.route("/refresh", methods=['POST'])
@limiter.limit('20 per minute')
@login_required(refresh=True) # instead of login_required
@inject
def refresh_route(
    current_user,
    jwt_service: JWTService = Provide[AppContainer.auth_container.jwt_service]
):
    try:
        access_token, refresh_token = jwt_service.create_auth_tokens(current_user.id)

        return generate_tokens_response(access_token, refresh_token)
    except UserNotFoundException:
        raise ApiNotFound(detail={"user": ["User not found"]})
    
@bp.route("/logout", methods=["POST"])
def logout_route():
    response = respond(data={"success": True})

    unset_jwt_cookies(response)

    return response

@bp.route("/oauth/yandex", methods=["POST"])
@inject
def oauth_yandex_route(
    yandex_oauth_service: YandexOauthService = Provide[AppContainer.auth_container.yandex_oauth_service],
    auth_service: AuthService = Provide[AppContainer.auth_container.auth_service],
    profile_auth_service: ProfileAuthService = Provide[AppContainer.profile_container.profile_auth_service]
):
    schema_data = AuthYandexOauthSchema().load(request.json)

    dto = AuthYandexOauthDTO(
        access_token=schema_data.get("access_token"),
        expires_in=schema_data.get("expires_in"),
        extra_data=schema_data.get("extra_data"),
        token_type=schema_data.get("token_type")
    )

    try:
        # Получает данные пользователя и если нет, то создает
        user, created, process_data = auth_service.system_process_yandex_oauth(dto)

        if created:

            avatar = None
            if not process_data.is_avatar_empty:
                avatar = yandex_oauth_service.get_user_avatar(process_data.default_avatar_id)

            profile_create_dto = ProfileCreateDTO(
                name=process_data.login,
                slug=f"{process_data.login}_{user.id}",
                about=None,
                avatar=avatar,
                creator_id=None,
                owner_id=user.id
            )

            profiles = [profile_auth_service.system_create_profile(profile_create_dto)]
        else:
            profiles = profile_auth_service.user_get_user_profiles(user)

        return respond(data=CurrentProfileSchema().dump(profiles, many=True))
    except Exception as e:
        raise e


