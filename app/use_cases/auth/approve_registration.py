from app.infrastructure.repositories import SQLUserRepository

class ApproveRegistration:
    def __init__(self, user_repo: SQLUserRepository):
        self.user_repo = user_repo

    def execute(self):
        pass