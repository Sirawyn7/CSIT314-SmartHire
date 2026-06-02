
from flask import Blueprint, render_template, session


class CandidateRoutes:
    """Handles candidate-facing page and API routes."""

    def __init__(self, db):
        self.db = db
        self.blueprint = Blueprint("candidate", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/candidate/profile", view_func=self.profile_page, methods=["GET"])

    def profile_page(self):
        """Renders the candidate profile page."""
        user_id = session.get("user_id")
        candidate = None

        if user_id:
            candidate = self.db.candidates.get_by_user_id(user_id)

        return render_template("candidate/profile.html", candidate=candidate)