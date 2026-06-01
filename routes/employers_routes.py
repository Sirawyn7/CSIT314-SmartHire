
from flask import Blueprint, render_template


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
        return render_template("employer/dashboard.html")