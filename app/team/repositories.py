from .models import Team

class TeamRepository:
    @staticmethod
    def create_team(team: Team):
        team.add(commit=True)

        return team