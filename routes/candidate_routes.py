
from flask import Blueprint, render_template


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
        return render_template("candidate/profile.html")