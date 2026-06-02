

import math
from flask import Blueprint, render_template, request
from config import JOBS_PER_PAGE


class JobRoutes:
    """Handles general job listing routes accessible to all users."""

    def __init__(self, db):
        self.db = db
        self.blueprint = Blueprint("jobs", __name__, url_prefix="/jobs")
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/", view_func=self.jobs_page, methods=["GET"])
        self.blueprint.add_url_rule("/<int:job_id>", view_func=self.job_details_page, methods=["GET"])


    def jobs_page(self):
        """Renders the paginated job listings page."""
        try:
            page = int(request.args.get("page", 1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1

        jobs, total = self.db.jobs.get_all_active_paginated(page, JOBS_PER_PAGE)
        total_pages = math.ceil(total / JOBS_PER_PAGE) if total > 0 else 1

        return render_template(
            "employer/jobs.html",
            jobs=jobs,
            page=page,
            total_pages=total_pages,
            total=total
        )
    
    def job_details_page(self, job_id):
        """Renders the details page for a single job."""
        job = self.db.jobs.get_by_id(job_id)
        if job is None:
            return render_template("error.html", message="Job not found."), 404
        return render_template("employer/job_details.html", job=job)