

from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify
from core.users_core import User, Candidate, Employer


class AuthRoutes:

    """Handles login, registration, and logout."""

    def __init__(self, db):
        self.db = db
        self.blueprint = Blueprint("auth", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/ping/auth", view_func=self.ping, methods=["GET"])
        self.blueprint.add_url_rule("/login", view_func=self.login_page, methods=["GET"])
        self.blueprint.add_url_rule("/register", view_func=self.register_page, methods=["GET"])
        self.blueprint.add_url_rule("/forgot-password", view_func=self.forgot_password_page, methods=["GET"])
        self.blueprint.add_url_rule("/api/auth/login", view_func=self.login_post, methods=["POST"])
        self.blueprint.add_url_rule("/api/auth/register", view_func=self.register_post, methods=["POST"])
        self.blueprint.add_url_rule("/api/auth/forgot-password", view_func=self.forgot_password_post, methods=["POST"])
        self.blueprint.add_url_rule("/api/auth/logout", view_func=self.logout, methods=["GET"])

    def ping(self):
        return jsonify({"message": "Auth routes are working"}), 200

    def login_page(self):
        return render_template("auth/login.html")

    def register_page(self):
        return render_template("auth/register.html")
    
    def forgot_password_page(self):
        return render_template("auth/forgot_password.html")
    
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

    def register_post(self):
        """Handles registration form submission, inserts user and logs in on success."""
        email = request.form.get("email")
        password = request.form.get("password")
        user_type = request.form.get("user_type")

        if self.db.users.get_by_email(email):
            return redirect(url_for("auth.forgot_password_page"))

        password_hash = User.hash_password(password)

        if user_type == "candidate":
            user = Candidate(
                user_data={
                    "email": email,
                    "password_hash": password_hash,
                    "user_type": user_type,
                    "is_member": 0,
                    "source": "registered"
                },
                profile_data={
                    "full_name": request.form.get("full_name"),
                    "phone": request.form.get("phone"),
                    "education": request.form.get("education"),
                    "field_of_study": request.form.get("field_of_study"),
                    "years_experience": request.form.get("years_experience"),
                    "skills": request.form.get("skills"),
                    "work_experience": request.form.get("work_experience"),
                    "preferred_work_mode": request.form.get("preferred_work_mode"),
                    "preferred_location": request.form.get("preferred_location"),
                    "source": "registered"
                }
            )

        elif user_type == "employer":
            user = Employer(
                user_data={
                    "email": email,
                    "password_hash": password_hash,
                    "user_type": user_type,
                    "is_member": 0,
                    "source": "registered"
                },
                profile_data={
                    "company_name": request.form.get("company_name"),
                    "company_description": request.form.get("company_description"),
                    "industry": request.form.get("industry"),
                    "location": request.form.get("location"),
                    "weburl": request.form.get("weburl"),
                    "contact_email": request.form.get("contact_email"),
                    "source": "registered"
                }
            )

        else:
            return render_template("auth/register.html", error="Invalid user type selected.")

        self.db.users.insert(user)

        user_row = self.db.users.get_by_email(email)

        session["user_id"] = user_row["id"]
        session["user_type"] = user_type

        if user_type == "candidate":
            return redirect(url_for("candidate.profile_page"))
        elif user_type == "employer":
            return redirect(url_for("employer.dashboard"))
    

    def forgot_password_post(self):
        """Handles forgot password form submission. Pseudo implementation — no email is sent."""
        email = request.form.get("email")

        user_row = self.db.users.get_by_email(email)

        if not user_row:
            return render_template("auth/forgot_password.html",
                error="No account found with that email address.")

        return render_template("auth/forgot_password.html",
            success=f"A password reset link has been sent to {email}.")
    

    def logout(self):
        """Clears the session and redirects to the login page."""
        session.clear()
        return redirect(url_for("auth.login_page"))