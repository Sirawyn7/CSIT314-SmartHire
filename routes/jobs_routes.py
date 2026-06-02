

import math
from flask import Blueprint, render_template, request
from config import JOBS_PER_PAGE, WORK_MODES, EDUCATION_LEVELS, JOB_KEYWORD_FIELDS
from core.search_core import SearchEngine


class JobRoutes:
    """Handles general job listing routes accessible to all users."""

    def __init__(self, db):
        self.db = db
        self.search_engine = SearchEngine()
        self.blueprint = Blueprint("jobs", __name__, url_prefix="/jobs")
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/", view_func=self.jobs_page, methods=["GET"])
        self.blueprint.add_url_rule("/<int:job_id>", view_func=self.job_details_page, methods=["GET"])


    def jobs_page(self):
        """Renders the paginated job listings page with optional keyword and filter search."""
        try:
            page = int(request.args.get("page", 1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1

        # Read search query
        query = request.args.get("q", "").strip()

        # Read filter args
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

        active_filters = {k: v for k, v in filters.items() if v is not None}
        all_jobs = self.db.jobs.get_all_active_with_employer()

        # Keyword first, then filter on the resulting subset
        if query:
            matched_jobs = self.search_engine.keyword_search(query, all_jobs, JOB_KEYWORD_FIELDS)
        else:
            matched_jobs = all_jobs

        if active_filters:
            matched_jobs = self.search_engine.filter_search(matched_jobs, filters)

        total = len(matched_jobs)
        total_pages = math.ceil(total / JOBS_PER_PAGE) if total > 0 else 1

        if page > total_pages:
            page = total_pages

        start = (page - 1) * JOBS_PER_PAGE
        end = start + JOBS_PER_PAGE
        jobs = matched_jobs[start:end]

        all_skills = self.db.jobs.get_all_unique_skills()

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
        return render_template("employer/job_details.html", job=job)