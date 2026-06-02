
from flask import Blueprint, render_template, session


class EmployerRoutes:
    """Handles employer-facing page and API routes."""

    def __init__(self, db):
        self.db = db
        self.blueprint = Blueprint("employer", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/employer/dashboard", view_func=self.dashboard, methods=["GET"])

    def dashboard(self):
        """Renders the employer dashboard page."""
        user_id = session.get("user_id")
        employer = None
        recent_jobs = []
        is_member = False

        if user_id:
            employer = self.db.employers.get_by_user_id(user_id)
            user = self.db.users.get_by_user_id(user_id)
            is_member = bool(user["is_member"]) if user else False

            if employer:
                recent_jobs = self.db.jobs.get_recent_by_employer_id(employer["id"], limit=4)

        return render_template(
            "employer/dashboard.html",
            employer=employer,
            recent_jobs=recent_jobs,
            is_member=is_member
        )