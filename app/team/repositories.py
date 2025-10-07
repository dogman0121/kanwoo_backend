from .models import Team, TeamAvatar, TeamLink

from typing import List

class TeamRepository:
    @staticmethod
    def create_team(team: Team):
        team.add()

        return team
    
    @staticmethod
    def delete_avatar(team: Team, avatar: TeamAvatar):
        team.avatar.delete()

        return team
    
    @staticmethod
    def update_avatar(team: Team, avatar: TeamAvatar):
        old_avatar = team.avatar

        team.avatar = avatar

        if old_avatar:
            old_avatar.delete(commit=True)

        return team


    @staticmethod
    def update_team(team: Team, data: dict):
        team.update(data)

        return team
    
    @staticmethod
    def add_links(team: Team, links: List[TeamLink]):
        old_links = team.links

        team.links = links

        for i in old_links:
            i.delete()

    @staticmethod
    def save_team(team: Team):
        team.save()