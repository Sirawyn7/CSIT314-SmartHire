

from config import MAX_RECOMMENDATIONS


class MembershipManager:
    """Determines recommendation limits based on user membership status."""

    def __init__(self, db):
        self.db = db

    def is_member(self, user_id):
        """Returns True if the user holds an active membership, False otherwise."""
        user = self.db.users.get_by_user_id(user_id)
        if not user:
            return False
        return bool(user["is_member"])

    def get_recommendation_limit(self, user_id):
        """Returns None (unlimited) for members, MAX_RECOMMENDATIONS for non-members."""
        return None if self.is_member(user_id) else MAX_RECOMMENDATIONS