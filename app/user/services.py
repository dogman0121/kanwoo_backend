from typing import Dict

from app.user.exceptions import (
    UserEmailAlreadyTakenException,
    UserLoginAlreadyTakenException,
    UserNotFoundException
)
from app.user.models import User
from app.user.repositories import UserRepository


class UserService:
    @staticmethod
    def get_by_id(user_id: int) -> User:
        user = UserRepository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException

        return user

    @staticmethod
    def get_by_login(login: str) -> User:
        user = UserRepository.get_by_login(login)

        if user is None:
            raise UserNotFoundException(f"User with login '{login}' not found")

        return user

    @staticmethod
    def get_by_email(email: str) -> User:
        user = UserRepository.get_by_email(email)

        if user is None:
            raise UserNotFoundException(f"User with email '{email}' not found")

        return user

    @staticmethod
    def create_user(user: User) -> User:
        if UserRepository.get_by_login(user.login):
            raise UserLoginAlreadyTakenException("Login already taken")

        if UserRepository.get_by_email(user.email):
            raise UserEmailAlreadyTakenException("Email already taken")

        user = UserRepository.create(user)

        return user

    @staticmethod
    def update_user(user: User, data: Dict) -> User:
        user.update(data)

        return user

