from pytils.translit import slugify
from werkzeug.datastructures import FileStorage
from typing import Optional

from .dto import TeamCreateDTO
from .models import Team
from .repositories import TeamRepository

from app import storage
from app.user.models import User


class TeamService:
    def __init__(self, user: User):
        self.user = user

    def create_team(self, data: TeamCreateDTO):
        slug = slugify(data.name)

        # check if slug has been taken
        i = 1
        while self.get_team_by_slug(slug):
            slug = slugify(data.name) + str(i)
            i+=1

        team = Team(
            name=data.name,
            slug=slug,
            about=data.about,
            creator_id=self.user.id,
        )

        TeamRepository.create_team(team)

        if data.poster:
            storage.save(data.poster, f'/teams/{team.id}', '.jpg')

        return team

    @staticmethod
    def get_team_by_slug(slug: str) -> Team:
        team = Team.query.filter_by(slug=slug).first()

        return team