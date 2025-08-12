from flask import request
from marshmallow import ValidationError

from app.exceptions import HTTPBadRequest
from app.utils import respond
from app.auth import bp
from app.auth.exceptions import AuthLoginAlreadyTakenException, AuthEmailAlreadyTakenException, \
    AuthPasswordNotMatchException, AuthUserWithLoginNotExistException
from app.auth.schemas import UserRegisterSchema
from app.auth.services import AuthService


@bp.route('/login', methods=['POST'])
def login_route():
    """ Login user. """
    login = request.json.get('login')
    password = request.json.get('password')

    try:
        access_token, refresh_token = AuthService.login_user(login, password)

        return respond(data={
            'access_token': access_token,
            'refresh_token': refresh_token,
        })
    except AuthPasswordNotMatchException:
        raise HTTPBadRequest(detail={"password": ["Invalid password"]})
    except AuthUserWithLoginNotExistException:
        raise HTTPBadRequest(detail={"login": ["Invalid login"]})


@bp.route('/register', methods=['POST'])
def register_route():
    """" Register new user. """
    register_schema = UserRegisterSchema()

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


@bp.route('/verify', methods=['POST'])
def verify_registration_route():
    token = request.json.get('token')

    if token is None:
        raise HTTPBadRequest(detail={"token": ["Invalid token"]})

    try:
        AuthService.verify_user_registration(token)


@bp.route('/forgot', methods=['POST'])
def forgot_password_route():
    raise NotImplementedError


@bp.route("/recovery", methods=['POST'])
def recovery_password_route():
    raise NotImplementedError