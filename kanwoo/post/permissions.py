class PostPolicy:

    def can_view_posts(self, profile, current_profile):
        return True