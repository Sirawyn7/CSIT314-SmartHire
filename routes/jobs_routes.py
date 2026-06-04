import math
from flask import Blueprint, render_template, request, redirect, session, url_for
from config import JOBS_PER_PAGE, WORK_MODES, EDUCATION_LEVELS, JOB_KEYWORD_FIELDS
from core.search_core import SearchEngine


class JobRoutes:
    """Handles general job listing routes accessible to all users."""

    def __init__(self, db):
        self.db = db
        self.search_engine = SearchEngine()
        self.blueprint = Blueprint("jobs", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/jobs/", view_func=self.jobs_page, methods=["GET"])
        self.blueprint.add_url_rule("/jobs/<int:job_id>", view_func=self.job_details_page, methods=["GET"])
        self.blueprint.add_url_rule("/jobs/<int:job_id>/apply", view_func=self.apply_to_job, methods=["POST"])

    def jobs_page(self):
        """Renders the paginated job listings page with keyword, fuzzy, and filter search."""
        try:
            page = int(request.args.get("page", 1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1

        query = request.args.get("q", "").strip()

        work_mode = request.args.get("work_mode", "").strip()
        education = request.args.get("education", "").strip()
        location = request.args.get("location", "").strip()
        skill = request.args.get("skill", "").strip()

        raw_experience = request.args.get("experience", "").strip()
        try:
            experience = int(raw_experience) if raw_experience else None
        except ValueError:
            experience = None

        filters = {
            "work_mode": work_mode or None,
            "education": education or None,
            "experience": experience,
            "location": location or None,
            "skill": skill or None,
        }

        all_jobs = self.db.jobs.get_all_active_with_employer()
        matched_jobs = self.search_engine.combined_search(query, all_jobs, JOB_KEYWORD_FIELDS, filters)

        total = len(matched_jobs)
        total_pages = math.ceil(total / JOBS_PER_PAGE) if total > 0 else 1

        if page > total_pages:
            page = total_pages

        start = (page - 1) * JOBS_PER_PAGE
        end = start + JOBS_PER_PAGE
        jobs = matched_jobs[start:end]

        all_skills = self.db.jobs.get_all_unique_skills()
        active_filters = {k: v for k, v in filters.items() if v is not None}

        return render_template(
            "employer/jobs.html",
            jobs=jobs,
            page=page,
            total_pages=total_pages,
            total=total,
            work_modes=WORK_MODES,
            education_levels=EDUCATION_LEVELS,
            all_skills=all_skills,
            active_filters=active_filters,
            selected_work_mode=work_mode,
            selected_education=education,
            selected_experience=raw_experience,
            selected_location=location,
            selected_skill=skill,
            query=query,
        )

    def job_details_page(self, job_id):
        """Renders the detail page for a single job."""
        job = self.db.jobs.get_by_id(job_id)
        if job is None:
            return render_template("error.html", message="Job not found."), 404

        user_id = session.get("user_id")
        user_type = session.get("user_type")
        is_job_owner = False

        if user_id and user_type == "employer":
            employer = self.db.employers.get_by_user_id(user_id)
            if employer and employer["id"] == job["employer_id"]:
                is_job_owner = True

        candidate = None
        application = None

        if user_id and user_type == "candidate":
            candidate = self.db.candidates.get_by_user_id(user_id)
            if candidate:
                application = self.db.applications.get_by_candidate_and_job(candidate["id"], job_id)

        return render_template(
            "employer/job_details.html",
            job=job,
            candidate=candidate,
            application=application,
            is_logged_in=bool(user_id),
            is_candidate=(user_type == "candidate"),
            applied=bool(request.args.get("applied")),
            updated=bool(request.args.get("updated")),
            apply_error=request.args.get("error", "").strip(),
            is_job_owner=is_job_owner,
            work_modes=WORK_MODES,
            education_levels=EDUCATION_LEVELS,
        )

    def apply_to_job(self, job_id):
        user_id = session.get("user_id")
        user_type = session.get("user_type")

        if not user_id:
            return redirect(url_for("auth.login_page"))

        if user_type != "candidate":
            return redirect(url_for("jobs.job_details_page", job_id=job_id, error="Only candidates can apply for jobs."))

        job = self.db.jobs.get_by_id(job_id)
        if job is None:
            return render_template("error.html", message="Job not found."), 404

        if not job["is_active"]:
            return redirect(url_for("jobs.job_details_page", job_id=job_id, error="This job is no longer accepting applications."))

        candidate = self.db.candidates.get_by_user_id(user_id)
        if not candidate:
            return redirect(url_for("jobs.job_details_page", job_id=job_id, error="Candidate profile not found."))
        
        existing_application = self.db.applications.get_by_candidate_and_job(candidate["id"], job_id)
        if existing_application and existing_application["status"] == "accepted":
            return redirect(
                url_for(
                    "jobs.job_details_page",
                    job_id=job_id,
                    error="You have already been accepted for this job."
                )
            )

        full_name = (request.form.get("full_name") or "").strip()
        if not full_name:
            return redirect(url_for("jobs.job_details_page", job_id=job_id, error="Full name is required."))

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

        _, created = self.db.applications.create_or_update(
            candidate["id"],
            job_id,
            request.form.get("cover_letter"),
        )

        if created:
            return redirect(url_for("jobs.job_details_page", job_id=job_id, applied=1))

        return redirect(url_for("jobs.job_details_page", job_id=job_id, updated=1))