from typing import Optional

from app.user.entities import UserEntity
from app.user.exceptions import UserEmailAlreadyTakenException, UserLoginAlreadyTakenException, UserNotFoundException
from app.user.repositories import UserRepository


class UserService:
    @staticmethod
    def get_by_id(user_id: int) -> UserEntity:
        user = UserRepository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException

        return user

    @staticmethod
    def get_by_login(login: str) -> UserEntity:
        user = UserRepository.get_by_login(login)

        if user is None:
            raise UserNotFoundException(f"User with login '{login}' not found")

        return user

    @staticmethod
    def get_by_email(email: str) -> UserEntity:
        user = UserRepository.get_by_email(email)

        if user is None:
            raise UserNotFoundException(f"User with email '{email}' not found")

        return user

    @staticmethod
    def create_user(user: UserEntity) -> UserEntity:
        if UserRepository.get_by_login(user.login):
            raise UserLoginAlreadyTakenException("Login already taken")

        if UserRepository.get_by_email(user.email):
            raise UserEmailAlreadyTakenException("Email already taken")

        user = UserRepository.create(user)

        return user

    @staticmethod
    def update_user(user: UserEntity) -> UserEntity:
        user = UserRepository.update(user)

        return user

