from pytils.translit import slugify
from werkzeug.datastructures import FileStorage

from app import storage
from app.team.schemas import TeamCreateSchema
from app.team.models import Team
from app.user.models import User


class TeamService:
    def __init__(self, user: User):
        self.user = user

    def create_team(self, data: TeamCreateSchema, poster: FileStorage):
        slug = slugify(data.name)

        # check if slug has been taken
        i = 1
        while self.get_team_by_slug(slug):
            slug = slugify(data.name) + str(i)

        team = Team(
            name=data.name,
            slug=slug,
            about=data.about,
            creator=self.user.id,
        )

        team.add(commit=True)

        storage.save(poster, f'/teams/{team.id}', '.jpg')

        return team

    @staticmethod
    def get_team_by_slug(slug: str) -> Team:
        team = Team.query.filter_by(slug=slug).first()

        return team