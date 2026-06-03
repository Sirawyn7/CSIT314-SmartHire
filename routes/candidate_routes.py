from flask import Blueprint, render_template, session, request, redirect, url_for


class CandidateRoutes:
    """Handles candidate-facing page and API routes."""

    def __init__(self, db):
        self.db = db
        self.blueprint = Blueprint("candidate", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/candidate/profile", view_func=self.profile_page, methods=["GET"])
        self.blueprint.add_url_rule("/candidate/profile/edit", view_func=self.edit_profile_post, methods=["POST"])
        self.blueprint.add_url_rule("/candidate/applications", view_func=self.applications_page, methods=["GET"])
        self.blueprint.add_url_rule("/candidate/applications/<int:application_id>/withdraw", view_func=self.withdraw_application_post, methods=["POST"])

    def profile_page(self):
        """Renders the candidate profile page."""
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login_page"))

        candidate = self.db.candidates.get_by_user_id(user_id)
        if not candidate:
            return redirect(url_for("auth.login_page"))

        user = self.db.users.get_by_user_id(user_id)
        is_member = bool(user["is_member"]) if user else False

        return render_template(
            "candidate/profile.html",
            candidate=candidate,
            is_member=is_member,
            updated=bool(request.args.get("updated"))
        )

    def edit_profile_post(self):
        """Updates the logged-in candidate profile."""
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login_page"))

        candidate = self.db.candidates.get_by_user_id(user_id)
        if not candidate:
            return redirect(url_for("auth.login_page"))

        self.db.candidates.update_by_user_id(
            user_id,
            {
                "full_name": request.form.get("full_name"),
                "phone": request.form.get("phone"),
                "education": request.form.get("education"),
                "field_of_study": request.form.get("field_of_study"),
                "years_experience": request.form.get("years_experience"),
                "skills": request.form.get("skills"),
                "work_experience": request.form.get("work_experience"),
                "preferred_work_mode": request.form.get("preferred_work_mode"),
                "preferred_location": request.form.get("preferred_location"),
            }
        )

        return redirect(url_for("candidate.profile_page", updated=1))
    
    def applications_page(self):
        """Renders the logged-in candidate's applied jobs page."""
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login_page"))

        candidate = self.db.candidates.get_by_user_id(user_id)
        if not candidate:
            return redirect(url_for("auth.login_page"))

        applications = self.db.applications.get_all_by_candidate_id(candidate["id"])

        return render_template(
            "candidate/applications.html",
            candidate=candidate,
            applications=applications,
        )
    
    def withdraw_application_post(self, application_id):
        """Marks an application as withdrawn for the logged-in candidate."""
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login_page"))

        candidate = self.db.candidates.get_by_user_id(user_id)
        if not candidate:
            return redirect(url_for("auth.login_page"))

        self.db.applications.update_status_by_id_and_candidate_id(
            application_id,
            candidate["id"],
            "withdrawn",
        )
        return redirect(url_for("candidate.applications_page"))