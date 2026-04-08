from sqlalchemy import func, select

from kanwoo import db
from kanwoo.repositories import BaseRepository
from kanwoo.models import Language, Privacy
from kanwoo.manga.models import Status, Type, Genre, Adult

from .models import Feedback

class MetaRepository(BaseRepository):

    def get_all_genres(self):
        return self.db_session.execute(select(Genre)).scalars().all()

    def get_all_statuses(self):
        return self.db_session.execute(select(Status)).scalars().all()

    def get_all_adults(self):
        return self.db_session.execute(select(Adult)).scalars().all()

    def get_all_types(self):
        return self.db_session.execute(select(Type)).scalars().all()

    def get_all_languages(self):
        return self.db_session.execute(select(Language)).scalars().all()

    def get_all_privacies(self):
        return self.db_session.execute(select(Privacy)).scalars().all()

class FeedbackRepository(BaseRepository):

    def create_feedback(self, feedback):
        feedback.add(commit=True)

        return feedback
    
    def get_unread_feedbacks_count(self):
        return self.db_session.execute(
            select(func.count("*"))
            .where(Feedback.resolved_at == None)    
        ).scalar()
    
    def update_feedback(self, feedback, data):
        feedback.update(data, commit=True)

        return feedback
    
    def get_feedback_by_id(self, feedback_id):
        return self.db_session.execute(select(Feedback).filter_by(id=feedback_id)).scalar()
    
    def get_feedbacks(self, resolved=None):
        q = select(Feedback)
        if resolved is None:
            pass
        else:
            if resolved:
                q = q.filter(Feedback.resolved_at.isnot(None))
            else:
                q.filter(Feedback.resolved_at.isnot(None))
        return self.db_session.execute(q.order_by(Feedback.created_at)).scalars().all()