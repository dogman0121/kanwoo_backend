from typing import Dict

from .exceptions import UserEmailAlreadyTakenException, UserNotFoundException
from .models import User
from .repositories import UserRepository
from .dto import UserCreateDTO


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

    def system_create_user(self, create_dto: UserCreateDTO) -> User:
        try:
            self.system_get_user_by_email(create_dto.email)

            raise UserEmailAlreadyTakenException("Email already taken")
        except UserNotFoundException:
            pass

        user = User(
            email=create_dto.email,
            password=create_dto.password_hash
        )

        return self.user_repo.create_user(user)

    def system_update_user(self, user: User, data: Dict) -> User:
        return self.user_repo.update_user(user, data)
