from app.infrastructure.repositories import SQLUserRepository


class GetAccessToken:
    def __init__(self, user_repo: SQLUserRepository, auth):
        self.user_repo = user_repo

