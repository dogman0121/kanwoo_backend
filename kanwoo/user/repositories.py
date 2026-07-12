from typing import Optional, Dict
from sqlalchemy import select, insert

from kanwoo.repositories import BaseRepository

from .models import User 

class UserRepository(BaseRepository):
    
    def create_user(self, user: User):
        user.add()

        return user

    def update_user(self, user: User, data: Dict) -> User:
        user.update(data)

        return user

    def get_by_id(self, user_id) -> Optional[User]:
        user = self.db_session.execute(select(User).filter_by(id=user_id)).scalar()

        return user

    def get_by_login(self, login: str) -> Optional[User]:
        user = self.db_session.execute(select(User).filter_by(login=login)).sclar()

        return user

    def get_by_email(self, email: str) -> Optional[User]:
        user = self.db_session.execute(select(User).filter_by(email=email)).scalar()

        return user