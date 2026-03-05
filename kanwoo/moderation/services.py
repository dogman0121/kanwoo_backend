from .repositories import MangaModerationRepository
from .dto import ModerationStatusUpdateDTO
from .models import MangaModerationStatus

class ModerationService:

    def __init__(self, manga_moderation_repo: MangaModerationRepository, chapter_moderation_repo):
        self.manga_moderation_repo = manga_moderation_repo
        self.chapter_moderation_repo = chapter_moderation_repo
    
    def _get_manga_waiting_moderation_count(self):
        return self.manga_moderation_repo.get_waiting_moderation_count()
    
    def _get_chapter_waiting_moderation_count(self):
        return self.chapter_moderation_repo.get_waiting_moderation_count()
    
    def _get_manga_moderation_history(self):
        pass

    def _update_manga_moderation_status(self, profile, manga, data: ModerationStatusUpdateDTO):
        moderation_status = MangaModerationStatus(
            manga_id=manga.id,
            status_type_id=data.status_type_id,
            message=data.message,
            creator_id=profile.id
        )

        self.manga_moderation_repo.add_moderation_status(moderation_status)

        return moderation_status

    def user_get_manga_waiting_moderation_count(self, profile):
        return self._get_manga_waiting_moderation_count()
    
    def user_get_manga_moderation_history(self, profile):
        return self._get_manga_moderation_history

    def user_get_chapter_waiting_moderation_count(self, profile):
        return self._get_chapter_waiting_moderation_count()
    
    def user_update_manga_moderation_status(self, profile, manga, data: ModerationStatusUpdateDTO):
        return self._update_manga_moderation_status(profile, manga, data)
    
    def system_update_manga_moderation_status(self, manga, data: ModerationStatusUpdateDTO):
        return self._update_manga_moderation_status(None, manga, data)