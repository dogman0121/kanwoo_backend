from app.domain.services.repository_service import RepositoryService
from old.user import User


class UserService(RepositoryService):
    def get_user_by_id(self, user_id: int) -> User:
        return self.repository.get_user_by_id(user_id)

    def get_user_by_login(self, login: str) -> User:
        return self.repository.get_user_by_login(login)

    def get_user_by_email(self, email: str) -> User:
        return self.repository.get_user_by_email(email)