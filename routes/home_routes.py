from flask import Blueprint, render_template

class HomeRoutes:

    def __init__(self):
        self.blueprint = Blueprint("home", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/home", view_func=self.home_page, methods=["GET"])

    def home_page(self):
        return render_template("home.html")