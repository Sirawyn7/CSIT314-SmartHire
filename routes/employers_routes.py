
from flask import Blueprint, render_template, session, redirect, url_for, request


class EmployerRoutes:
    """Handles employer-facing page and API routes."""

    def __init__(self, db):
        self.db = db
        self.blueprint = Blueprint("employer", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/employer/dashboard", view_func=self.dashboard, methods=["GET"])
        self.blueprint.add_url_rule("/employer/dashboard/edit", view_func=self.edit_dashboard_post, methods=["POST"])
        self.blueprint.add_url_rule("/employer/jobs", view_func=self.manage_jobs, methods=["GET"])
        self.blueprint.add_url_rule("/employer/jobs/<int:job_id>/deactivate", view_func=self.deactivate_job, methods=["POST"])
        self.blueprint.add_url_rule("/employer/jobs/<int:job_id>/reactivate", view_func=self.reactivate_job, methods=["POST"])
        self.blueprint.add_url_rule("/employer/jobs/<int:job_id>/applications",view_func=self.job_applications_page,methods=["GET"])
        self.blueprint.add_url_rule("/employer/applications/<int:application_id>/status",view_func=self.update_application_status,methods=["POST"])

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
            is_member=is_member,
            updated=bool(request.args.get("updated"))
        )
    
    def edit_dashboard_post(self):
        """Updates the logged-in employer profile."""
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login_page"))

        employer = self.db.employers.get_by_user_id(user_id)
        if not employer:
            return redirect(url_for("auth.login_page"))

        self.db.employers.update_by_user_id(
            user_id,
            {
                "company_name": request.form.get("company_name"),
                "company_description": request.form.get("company_description"),
                "industry": request.form.get("industry"),
                "location": request.form.get("location"),
                "weburl": request.form.get("weburl"),
                "contact_email": request.form.get("contact_email"),
            }
        )

        return redirect(url_for("employer.dashboard", updated=1))
        
    def manage_jobs(self):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        employer = self.db.employers.get_by_user_id(user_id)
        if not employer:
            return redirect(url_for("employer.dashboard"))
        all_jobs = self.db.jobs.get_all_by_employer_id(employer["id"])
        active_jobs = [j for j in all_jobs if j["is_active"] == 1]
        inactive_jobs = [j for j in all_jobs if j["is_active"] == 0]
        tab = request.args.get("tab", "active")
        return render_template(
            "employer/manage_jobs.html",
            employer=employer,
            active_jobs=active_jobs,
            inactive_jobs=inactive_jobs,
            tab=tab
        )
    
    def deactivate_job(self, job_id):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        employer = self.db.employers.get_by_user_id(user_id)
        if employer:
            self.db.jobs.set_active_status(job_id, employer["id"], 0)
        return redirect(url_for("employer.manage_jobs", tab="active"))
    
    def reactivate_job(self, job_id):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login"))
        employer = self.db.employers.get_by_user_id(user_id)
        if employer:
            self.db.jobs.set_active_status(job_id, employer["id"], 1)
        return redirect(url_for("employer.manage_jobs", tab="inactive"))
    
    def job_applications_page(self, job_id):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login_page"))

        employer = self.db.employers.get_by_user_id(user_id)
        if not employer:
            return redirect(url_for("employer.dashboard"))

        job = self.db.jobs.get_by_id(job_id)
        if not job or job["employer_id"] != employer["id"]:
            return render_template("error.html", message="Job not found."), 404

        applications = self.db.applications.get_all_by_job_id_and_employer_id(job_id, employer["id"])

        return render_template(
            "employer/job_applications.html",
            employer=employer,
            job=job,
            applications=applications,
            updated=bool(request.args.get("updated")),
        )

    def update_application_status(self, application_id):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("auth.login_page"))

        employer = self.db.employers.get_by_user_id(user_id)
        if not employer:
            return redirect(url_for("employer.dashboard"))

        status = (request.form.get("status") or "").strip().lower()
        allowed_statuses = {"pending", "reviewed", "contacted", "rejected", "accepted"}
        if status not in allowed_statuses:
            return redirect(url_for("employer.dashboard"))

        job_id = self.db.applications.update_status_by_id_and_employer_id(
            application_id,
            employer["id"],
            status,
        )

        if not job_id:
            return render_template("error.html", message="Application not found."), 404

        return redirect(url_for("employer.job_applications_page", job_id=job_id, updated=1))