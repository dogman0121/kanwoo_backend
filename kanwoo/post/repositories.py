from sqlalchemy import select

from kanwoo.repositories import BaseRepository
from kanwoo.models import cursor_paginate

from .models import Post

class PostRepository(BaseRepository):
    model = Post

    def get_profile_posts(self, profile, cursor, limit):
        query = select(Post).filter_by(creator_id = profile.id)

        results, total_count, new_cursor = cursor_paginate(
            Post, 
            self.db_session, 
            query, 
            None, 
            cursor=cursor, 
            limit=limit
        )

        return results, total_count, new_cursor