
from flask import Blueprint, render_template


class AdminRoutes:
    """Handles admin-facing page and API routes."""

    def __init__(self, db):
        self.db = db
        self.blueprint = Blueprint("admin", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/admin/panel", view_func=self.panel, methods=["GET"])

    def panel(self):
        """Renders the admin panel page."""
        return render_template("admin/panel.html")