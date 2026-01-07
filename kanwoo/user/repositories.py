from typing import Optional, Dict

from app.user.models import User


class UserRepository:
    @staticmethod
    def create(user: User):
        user.add()

        return user

    @staticmethod
    def update(user: User, data: Dict) -> User:
        user.update(data)

        return user

    @staticmethod
    def get_by_id(user_id) -> Optional[User]:
        user = User.query.get(user_id)

        return user

    @staticmethod
    def get_by_login(login: str) -> Optional[User]:
        user = User.query.filter_by(login=login).first()

        return user

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        user = User.query.filter_by(email=email).first()

        return user