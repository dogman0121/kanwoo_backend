from typing import Dict

from kanwoo.user.exceptions import UserEmailAlreadyTakenException, UserLoginAlreadyTakenException, UserNotFoundException
from kanwoo.user.models import User
from kanwoo.user.repositories import UserRepository


class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def system_get_user_by_id(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException

        return user

    def get_by_login(self, login: str) -> User:
        user = self.user_repo.get_by_login(login)

        if user is None:
            raise UserNotFoundException(f"User with login '{login}' not found")

        return user

    def get_by_email(self, email: str) -> User:
        user = self.user_repo.get_by_email(email)

        if user is None:
            raise UserNotFoundException(f"User with email '{email}' not found")

        return user

    def create_user(self, user: User) -> User:
        if self.user_repo.get_by_login(user.login):
            raise UserLoginAlreadyTakenException("Login already taken")

        if self.user_repo.get_by_email(user.email):
            raise UserEmailAlreadyTakenException("Email already taken")

        user = self.user_repo.create_user(user)

        return user

    def update_user(self, user: User, data: Dict) -> User:
        return self.user_repo.update_user(user, data)
