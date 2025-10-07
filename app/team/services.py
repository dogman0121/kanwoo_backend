from pytils.translit import slugify

from .dto import TeamCreateDTO, TeamUpdateDTO
from .models import Team, TeamAvatar, TeamLink
from .repositories import TeamRepository
from .exceptions import TeamNotFoundException, TeamUpdateNotAllowedException
from .permissions import TeamPolicy
from .schemas import AvatarAction

from app import storage
from app.uuid import UUID
from app.user.models import User


class TeamService:
    def __init__(self, user: User):
        self.user = user

    def create_team(self, data: TeamCreateDTO):
        if data.avatar:
            avatar_uuid = UUID.generate_uuid()
            
            storage.save(data.avatar, f'teams/{team.id}/{avatar_uuid}.jpg')
        
        
        slug = slugify(data.name)

        # check if slug has been taken
        try:
            i = 1
            while self.get_team_by_slug(slug):
                slug = slugify(data.name) + str(i)
                i+=1
        except TeamNotFoundException:
            pass

        team = Team(
            name=data.name,
            slug=slug,
            about=data.about,
            creator_id=self.user.id,
        )

        TeamRepository.create_team(team)

        if data.avatar:
            avatar = TeamAvatar(
                uuid=avatar_uuid,
                orig_filename=data.avatar.filename,
                ext=".jpg"
            )

            team = TeamRepository.update_avatar(team, avatar)

        TeamRepository.save_team(team)

        return team
    

    def update_team(self, team: Team, data: TeamUpdateDTO):
        if not TeamPolicy(self.user).can_edit(team):
            raise TeamUpdateNotAllowedException

        if data.avatar_action == AvatarAction.REMOVE:
            storage.delete(f'teams/{team.id}/{team.avatar.uuid}{team.avatar.ext}')
            team = TeamRepository.delete_avatar(team, team.avatar)

        elif data.avatar_action == AvatarAction.UPDATE:
            old_avatar = team.avatar
            
            new_avatar_uuid = UUID.generate_uuid()
            storage.save(data.avatar, f'teams/{team.id}/{new_avatar_uuid}.jpg')
            
            new_avatar = TeamAvatar(
                uuid=new_avatar_uuid,
                orig_filename=data.avatar.filename,
                ext=".jpg"
            )

            team = TeamRepository.update_avatar(team, new_avatar)

            if old_avatar:
                storage.delete(f'teams/{team.id}/{old_avatar.uuid}.jpg')

        if data.links:
            links = [
                TeamLink(
                    name=l.name,
                    link=l.link
                ) for l in data.links
            ]
        else:
            links = []

        team = TeamRepository.update_team(team, {
            "name": data.name,
            "slug": data.slug,
            "about": data.about,
        })

        TeamRepository.add_links(team, links)

        TeamRepository.save_team(team)

        return team
        

    @staticmethod
    def get_team_by_slug(slug: str) -> Team:
        team = Team.query.filter_by(slug=slug).first()

        if team is None:
            raise TeamNotFoundException

        return team