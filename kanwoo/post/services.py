from kanwoo.database import DBTransaction

from .repositories import PostRepository
from .permissions import PostPolicy


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