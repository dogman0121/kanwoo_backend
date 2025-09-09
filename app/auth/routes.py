from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import set_refresh_cookies
from marshmallow import ValidationError

from app import limiter
from app.exceptions import HTTPBadRequest, HTTPNotFound
from app.auth.middleware import login_required
from app.user.exceptions import UserNotFoundException
from app.user.services import UserService
from app.user.utils import get_current_user
from app.utils import respond
from app.auth import bp
from app.auth.exceptions import AuthLoginAlreadyTakenException, AuthEmailAlreadyTakenException, \
    AuthPasswordNotMatchException, AuthUserWithLoginNotExistException, AuthJWTTokenExpiredException, \
    AuthUserWithEmailNotExistException
from app.auth.schemas import AuthRegisterSchema, AuthRecoverySchema
from app.auth.services import AuthService, generate_auth_tokens

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
def login_route():
    """ Login user. """
    login = request.json.get('login')
    password = request.json.get('password')

    try:
        access_token, refresh_token = AuthService.login_user(login, password)

        return generate_tokens_response(access_token, refresh_token)
    except AuthPasswordNotMatchException:
        raise HTTPBadRequest(detail={"password": ["Invalid password"]})
    except AuthUserWithLoginNotExistException:
        raise HTTPBadRequest(detail={"login": ["Invalid login"]})


@bp.route('/register', methods=['POST'])
@limiter.limit('3 per minute')
def register_route():
    """" Register new user. """
    register_schema = AuthRegisterSchema()

    try:
        data = register_schema.load({
            "login": request.json.get('login'),
            "email": request.json.get('email'),
            "password": request.json.get('password')
        })

        AuthService.register_user(login=data['login'], email=data['email'], password=data['password'])

        return respond(data={
            "success": True,
        }, status_code=201)
    except ValidationError as e:
        raise HTTPBadRequest(detail=e.messages)
    except AuthLoginAlreadyTakenException as e:
        raise HTTPBadRequest(detail={"login": ["Login already taken"]})
    except AuthEmailAlreadyTakenException as e:
        raise HTTPBadRequest(detail={"email": ["Email already taken"]})


@bp.route('/verify', methods=['GET'])
@limiter.limit('5 per minute')
@login_required
def get_verification_message_route():
    """ Get user account verification message. """
    user_id = get_current_user()

    try:
        user = UserService.get_by_id(user_id)

        AuthService.send_verification_email(user)

        return respond(data={
            "success": True,
        })
    except UserNotFoundException:
        raise HTTPNotFound(detail={"user": ["User not found"]})

@bp.route('/verify', methods=['POST'])
@limiter.limit('3 per minute')
def verify_registration_route():
    token = request.json.get('token')

    if token is None:
        raise HTTPBadRequest(detail={"token": ["Token is required"]})

    try:
        access_token, refresh_token = AuthService.verify_user_registration(token)

        return generate_tokens_response(access_token, refresh_token)
    except AuthJWTTokenExpiredException:
        raise HTTPBadRequest(detail={"token": ["Token expired"]})


@bp.route('/forgot', methods=['POST'])
@limiter.limit('5 per minute')
def forgot_password_route():
    email = request.json.get('email')

    try:
        AuthService.send_recovery_message(email)

        return respond(data={"success": True})
    except AuthUserWithEmailNotExistException:
        raise HTTPBadRequest(detail={"email": ["Invalid email"]})


@bp.route("/recovery", methods=['POST'])
@limiter.limit('5 per minute')
def recovery_password_route():
    recovery_schema = AuthRecoverySchema()

    data = recovery_schema.load({
        "token": request.json.get('token'),
        "old_password": request.json.get('old_password'),
        "new_password": request.json.get('new_password'),
    })

    try:
        AuthService.update_password(data["token"], data["old_password"], data["new_password"])

        return respond(data={'success': True})
    except AuthPasswordNotMatchException:
        raise HTTPBadRequest(detail={"password": ["Invalid password"]})
    except AuthJWTTokenExpiredException:
        raise HTTPBadRequest(detail={"token": ["Token expired"]})


@bp.route("/refresh", methods=['POST'])
@limiter.limit('20 per minute')
@jwt_required(refresh=True) # instead of login_required
def refresh_route():
    try:
        current_user = get_current_user()

        access_token, refresh_token = generate_auth_tokens(current_user)

        return generate_tokens_response(access_token, refresh_token)
    except UserNotFoundException:
        raise HTTPNotFound(detail={"user": ["User not found"]})