

from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify
from core.users_core import User


class AuthRoutes:

    """Handles login, registration, and logout."""

    def __init__(self, db):
        self.db = db
        self.blueprint = Blueprint("auth", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/base", view_func=self.base, methods=["GET"])
        self.blueprint.add_url_rule("/ping/auth", view_func=self.ping, methods=["GET"])
        self.blueprint.add_url_rule("/login", view_func=self.login_page, methods=["GET"])
        self.blueprint.add_url_rule("/register", view_func=self.register_page, methods=["GET"])
        self.blueprint.add_url_rule("/forgot-password", view_func=self.forgot_password_page, methods=["GET"])
        self.blueprint.add_url_rule("/api/auth/login", view_func=self.login_post, methods=["POST"])
        self.blueprint.add_url_rule("/api/auth/register", view_func=self.register, methods=["POST"])
        self.blueprint.add_url_rule("/api/auth/forgot-password", view_func=self.forgot_password_submit, methods=["POST"])
        self.blueprint.add_url_rule("/api/auth/logout", view_func=self.logout, methods=["POST"])

    def base(self):
        return render_template("base.html")

    def ping(self):
        return jsonify({"message": "Auth routes are working"}), 200

    def login_page(self):
        return render_template("login.html")

    def register_page(self):
        return render_template("register.html")
    
    def forgot_password_page(self):
        return render_template("forgot_password.html")
    

    def login_post(self):
        """Handles login form submission, creates session on success."""
        email = request.form.get("email")
        password = request.form.get("password")

        user_row = self.db.users.get_by_email(email)

        if not user_row or not User.check_password(password, user_row["id"], self.db):
            return render_template("auth/login.html", error="Invalid email or password.")

        session["user_id"] = user_row["id"]
        session["user_type"] = user_row["user_type"]

        if user_row["user_type"] == "candidate":
            return redirect(url_for("candidate.profile_page"))
        elif user_row["user_type"] == "employer":
            return redirect(url_for("employer.dashboard"))
        elif user_row["user_type"] == "admin":
            return redirect(url_for("admin.panel"))
        else:
            session.clear()
            return render_template("auth/login.html", error="Login failed. Please contact support.")

    def register(self):
        data = request.get_json()


        # Call users database to verify not already registered, then inserts new user


        return jsonify({"message": "User registered"}), 201
    

    def forgot_password_submit(self):
        data = request.get_json()

        # Password reset logic here

        return jsonify({"message": "Reset link sent"}), 200
    

    def logout(self):
        """Clears the session and redirects to the login page."""
        session.clear()
        return redirect(url_for("auth.login_page"))