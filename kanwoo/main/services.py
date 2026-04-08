from datetime import datetime

from .dto import MetaDTO, MetaMainDTO, MetaMangaDTO
from .models import Feedback
from .repositories import FeedbackRepository, MetaRepository

class MetaService:

    def __init__(self, meta_repo: MetaRepository):
        self.meta_repo = meta_repo
    
    def user_get_meta(self):
        statuses = self.meta_repo.get_all_statuses()
        types = self.meta_repo.get_all_types()
        genres = self.meta_repo.get_all_genres()
        adults = self.meta_repo.get_all_adults()

        privacies = self.meta_repo.get_all_privacies()
        languages = self.meta_repo.get_all_languages()

        return MetaDTO(
            main=MetaMainDTO(
                privacies=privacies,
                languages=languages
            ),
            manga=MetaMangaDTO(
                statuses=statuses,
                types=types,
                genres=genres,
                adults=adults
            )
        )

class FeedbackService:

    def __init__(self, feedback_repo: FeedbackRepository):
        self.feedback_repo = feedback_repo
    
    def user_create_feedback(self, profile, data):
        feedback = Feedback(
            message=data.message
        )

        if profile:
            feedback.creator_id = profile.id

        return self.feedback_repo.create_feedback(feedback)
    
    def user_get_feedbacks(self, profile, resolved=None):
        return self.feedback_repo.get_feedbacks(resolved=resolved)

    def user_get_feedback_by_id(self, profile, feedback_id):
        return self.feedback_repo.get_feedback_by_id(feedback_id)   
    
    def user_get_unread_feedback_count(self, profile):
        return self.feedback_repo.get_unread_feedbacks_count()
    
    def user_resolve_feedback(self, profile, feedback):
        self.feedback_repo.update_feedback(feedback, {
            "resolved_at": datetime.now(),
            "resolver_id": profile.id
            }
        )

        return feedback