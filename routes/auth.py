

from flask import Blueprint, jsonify, request, render_template


class AuthRoutes:
    def __init__(self, db):
        self.db = db
        self.blueprint = Blueprint("auth", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/ping/auth", view_func=self.ping, methods=["GET"])
        self.blueprint.add_url_rule("/login", view_func=self.login_page, methods=["GET"])
        self.blueprint.add_url_rule("/register", view_func=self.register_page, methods=["GET"])
        self.blueprint.add_url_rule("/forgot-password", view_func=self.forgot_password_page, methods=["GET"])
        self.blueprint.add_url_rule("/api/auth/login", view_func=self.login, methods=["POST"])
        self.blueprint.add_url_rule("/api/auth/register", view_func=self.register, methods=["POST"])
        self.blueprint.add_url_rule("/api/auth/forgot-password", view_func=self.forgot_password_submit, methods=["POST"])
        self.blueprint.add_url_rule("/api/auth/logout", view_func=self.logout, methods=["POST"])

    def ping(self):
        return jsonify({"message": "Auth routes are working"}), 200

    def login_page(self):
        return render_template("login.html")

    def register_page(self):
        return render_template("register.html")
    
    def forgot_password_page(self):
        return render_template("forgot_password.html")
    

    def login(self):
        data = request.get_json()


        # Call users database to verify that login credentials are correct


        return jsonify({"message": "Login successful"}), 200

    def register(self):
        data = request.get_json()


        # Call users database to verify not already registered, then inserts new user


        return jsonify({"message": "User registered"}), 201
    

    def forgot_password_submit(self):
        data = request.get_json()

        # Password reset logic here

        return jsonify({"message": "Reset link sent"}), 200
    

    def logout(self):

        # Logout functionality


        return jsonify({"message": "Logged out"}), 200