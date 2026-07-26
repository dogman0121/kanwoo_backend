from sqlalchemy import select, insert

from kanwoo.user.models import User
from kanwoo.repositories import BaseRepository

from .entity import OauthTypeEnum
from .models import Oauth

class AuthRepository(BaseRepository):
    def get_user_by_oauth(self, user_id, oauth_type: OauthTypeEnum):
        user = self.db_session.execute(
            select(User)
            .join(Oauth, User.id==Oauth.c.user_id)
            .filter(
                Oauth.c.oauth_type_id==oauth_type.value, 
                Oauth.c.oauth_id==user_id
            )
        ).scalar()

        return user
    
    def add_oauth_verification(self, user, oauth_user_id, oauth_user_type):
        self.db_session.execute(
            insert(Oauth)
            .values(
                user_id=user.id,
                oauth_type_id=oauth_user_type.value,
                oauth_id=oauth_user_id
            )
        )