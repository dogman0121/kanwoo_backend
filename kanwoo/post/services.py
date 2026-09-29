from kanwoo.database import DBTransaction
from kanwoo.exceptions import ApiForbidden

from .repositories import PostRepository
from .permissions import PostPolicy
from .dto import PostCreateDTO
from .models import Post

class PostService:

    def __init__(
        self,
        post_repo: PostRepository,
        post_policy: PostPolicy,
        db_transaction: DBTransaction
    ):
        self.post_repo = post_repo
        self.post_policy = post_policy
        self.db_trasaction = db_transaction

    def user_get_post_by_id(self, profile, post_id):
        return self.post_repo.get_by_id(post_id)

    def user_create_post(self, profile, post_data: PostCreateDTO):

        with self.db_trasaction:
            post = Post(
                text = post_data.text,
                creator_id = profile.id
            )

            self.post_repo.add(post)

            return post

    def user_get_profile_posts(self, profile, current_profile, cursor, limit):
        if not self.post_policy.can_view_posts(profile, current_profile):
            raise ApiForbidden()
        
        posts, total_count, new_last_id = self.post_repo.get_user_posts(profile, cursor, limit)

        return posts, total_count, new_last_id
