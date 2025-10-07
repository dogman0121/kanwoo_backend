from .models import Team
from app.user.models import User

class TeamPolicy:
    def __init__(self, user: User):
        self.user = user

    def can_edit(self, team: Team):
        if self.user.id == team.creator_id:
            return True
        
        return False