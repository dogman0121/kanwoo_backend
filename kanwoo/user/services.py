from typing import Dict

from kanwoo.user.exceptions import UserEmailAlreadyTakenException, UserNotFoundException
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

    def system_get_user_by_email(self, email: str) -> User:
        user = self.user_repo.get_by_email(email)

        if user is None:
            raise UserNotFoundException(f"User with email '{email}' not found")

        return user

    def system_create_user(self, user: User) -> User:
        if self.user_repo.get_by_email(user.email):
            raise UserEmailAlreadyTakenException("Email already taken")

        user = self.user_repo.create_user(user)

        return user

    def system_update_user(self, user: User, data: Dict) -> User:
        return self.user_repo.update_user(user, data)
