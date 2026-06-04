from flask import Blueprint, render_template


class HomeRoutes:
    """
    Manages routes related to the homepage.
    """

    def __init__(self, db):
        # Store database reference for consistency with other route classes
        self.db = db

        # Create Flask blueprint for homepage routes
        self.blueprint = Blueprint("home", __name__)

        # Register all homepage routes
        self._register_routes()

    def _register_routes(self):
        """
        Register homepage endpoints.
        """
        self.blueprint.add_url_rule("/home", view_func=self.home_page, methods=["GET"])

    def home_page(self):
        """
        Render the Smart Hire homepage.
        """
        return render_template("home.html")