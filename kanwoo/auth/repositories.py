from sqlalchemy import select, insert

from kanwoo.user.models import User
from kanwoo.repositories import BaseRepository

from .entity import OauthTypeEnum
from .models import Oauth

class AuthRepository(BaseRepository):
    def get_user_by_oauth(self, user_id, oauth_type: OauthTypeEnum):
        user = self.db_session.execute(
            select(User)
            .join(Oauth, User.id==Oauth.user_id)
            .filter(
                Oauth.oauth_type_id==oauth_type.value, 
                Oauth.oauth_user_id==user_id
            )
        ).scalar()

        return user
    
    def add_oauth(self, oauth):
        oauth.add()

        return oauth