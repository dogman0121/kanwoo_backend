from abc import ABC, abstractmethod

from old.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_by_login(self, login: str) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass