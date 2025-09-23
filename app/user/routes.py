from flask import jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)
from app import storage
from app.user import bp
from app.user.models import User, Avatar
from app.notifications.models import Notification
from PIL import Image

from app.user.utils import get_current_user
from app.utils import respond
from app.auth.middleware import login_required
from app.user.schemas import UserMeSchema


@bp.route('/v1/users/<int:user_id>', methods=['GET'])
@jwt_required(optional=True)
def get_user_v1(user_id: int):
    user = User.get_by_id(user_id)
    current_user = User.get_by_id(get_jwt_identity())

    if user is None:
        return jsonify(data=None, error={"code": "not_found"}), 404
    return jsonify(data = user.to_dict(user=current_user)), 200

@bp.route('/v1/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_v1(user_id: int):
    user = User.get_by_id(user_id)
    current_user = User.get_by_id(get_jwt_identity())

    if user.id != current_user.id:
        return jsonify(data=None, error={"code": "forbidden"}), 403

    avatar = request.files.get('avatar')
    if avatar is not None:
        new_file = Image.open(avatar).convert('RGB')
        new_file.filename = avatar.filename
        new_file.thumbnail((120, 120))

        filename = storage.save(new_file, f"user/{user_id}", ext=".jpg")

        if user.avatar is not None:
            storage.delete(f"user/{user.id}/{user.avatar.filename}")
            user.avatar.filename = filename + ".jpg"
        else:
            user.avatar = Avatar(filename=filename + ".jpg")

    login = request.form.get('login')
    if login is not None:
        user.login = login

    about = request.form.get('about')
    if about is not None:
        user.about = about

    user.update()

    return jsonify(data=user.to_dict(current_user)), 200


@bp.route('/v1/users/<int:user_id>/subscribe', methods=['POST', 'DELETE'])
@jwt_required()
def subscribe_v1(user_id: int):
    user = User.get_by_id(user_id)
    subscriber = User.get_by_id(get_jwt_identity())

    if user.id == subscriber.id:
        return jsonify(data=None, error={"code": "forbidden"}), 403

    if user is None:
        return jsonify(data=None, error={"code": "not_found"}), 404

    if subscriber is None:
        return jsonify(data=None, error={"code": "not_found"}), 404

    if request.method == 'POST':
        user.subscribe(subscriber)
        notification = Notification(
            action="subscribe",
            user=user,
            actor=subscriber
        )
        notification.add()
        return jsonify({"error": None, "data": None}), 200
    elif request.method == 'DELETE':
        user.unsubscribe(subscriber)
        return jsonify({"error": None, "data": None}), 200

@bp.route('/v1/users/<int:user_id>/subscribers', methods=['GET'])
@jwt_required(optional=True)
def get_subscribers_v1(user_id: int):
    user = User.get_by_id(user_id)

    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id) if current_user_id else None

    page = request.args.get('page', 1, type=int)

    if user is None:
        return jsonify(data=None, error={"code": "not_found"}), 404

    subscribers = user.get_subscribers(page=page, per_page=20)

    return jsonify(data=[i.to_dict(current_user) for i in subscribers]), 200

@bp.route('/v1/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def edit_user_v1(user_id: int):
    user = User.get_by_id(int(get_jwt_identity()))

    if user.id != user_id:
        return respond(error="forbidden", detail={"msg": "You are not allowed to edit this user"}), 403

    if "login" in request.json:
        user.login = request.json["login"]

    if "password" in request.json:
        user.password = request.json["password"]

    user.update()
    return respond(data=user.to_dict())


@bp.route('/v1/users/me', methods=['GET'])
@login_required()
def me_route(user):
    schema = UserMeSchema()

    print(user.subscribers_count)
    print(user.id)

    return respond(data=schema.dump(user))


@bp.route('/v1/users/me/affiliate', methods=['GET'])
def affiliate_user_v1(user_id: int):
    pass