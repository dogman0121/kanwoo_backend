from typing import Optional

from app import db
from app.user.entities import UserEntity
from app.user.models import User


def _entity_to_model(entity: UserEntity):
    return User(
        id=entity.id,
        login=entity.login,
        email=entity.email,
        password=entity.password,
        is_verified=entity.is_verified,
    )

def _model_to_entity(model: User):
    return UserEntity(
        id=model.id,
        login=model.login,
        email=model.email,
        password=model.password,
        is_verified=model.is_verified,
    )

class UserRepository:
    @staticmethod
    def create(user: UserEntity):
        user_model = _entity_to_model(user)

        db.session.add(user_model)
        db.session.commit()

        return _model_to_entity(user_model)

    @staticmethod
    def update(user: UserEntity) -> UserEntity:
        user_model = _entity_to_model(user)

        db.session.commit()

        return _model_to_entity(user_model)

    @staticmethod
    def get_by_id(user_id) -> Optional[UserEntity]:
        user_model = User.query.get(user_id).first()

        if user_model is None:
            return None

        return _model_to_entity(user_model)

    @staticmethod
    def get_by_login(login: str) -> Optional[UserEntity]:
        user_model = User.query.filter_by(login=login).first()

        if user_model is None:
            return None

        return _model_to_entity(user_model)

    @staticmethod
    def get_by_email(email: str) -> Optional[UserEntity]:
        user_model = User.query.filter_by(email=email).first()

        if user_model is None:
            return None

        return _model_to_entity(user_model)