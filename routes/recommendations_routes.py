
from flask import Blueprint, render_template, redirect, url_for, session, abort
from core.matcher_core import Matcher
from core.membership_core import MembershipManager


class RecommendationRoutes:
    """Handles recommendation pages for candidates and employers."""

    def __init__(self, db):
        self.db         = db
        self.blueprint  = Blueprint("recommendations", __name__)
        self.matcher    = Matcher()
        self.membership = MembershipManager(db)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/recommendations/jobs", view_func=self.candidate_recommendations, methods=["GET"])
        self.blueprint.add_url_rule("/recommendations/candidates/<int:job_id>", view_func=self.employer_recommendations, methods=["GET"])

    def candidate_recommendations(self):
        """Renders recommended jobs for the logged-in candidate."""
        if session.get("user_type") != "candidate":
            return redirect(url_for("auth.login_page"))

        user_id   = session["user_id"]
        limit     = self.membership.get_recommendation_limit(user_id)
        is_member = self.membership.is_member(user_id)

        candidate = self.db.candidates.get_by_user_id(user_id)
        all_jobs  = self.db.jobs.get_all_active()
        results   = self.matcher.recommend_jobs_for_candidate(candidate, all_jobs, limit)

        return render_template(
            "candidate/recommendations.html",
            results=results,
            candidate=candidate,
            is_member=is_member,
            limit=limit,
        )

    def employer_recommendations(self, job_id):
        """Renders recommended candidates for a specific job listing."""
        if session.get("user_type") != "employer":
            return redirect(url_for("auth.login_page"))

        user_id  = session["user_id"]
        employer = self.db.employers.get_by_user_id(user_id)
        job      = self.db.jobs.get_by_id(job_id)

        if not job or job["employer_id"] != employer["id"]:
            abort(403)

        limit     = self.membership.get_recommendation_limit(user_id)
        is_member = self.membership.is_member(user_id)

        all_candidates = self.db.candidates.get_all()
        results        = self.matcher.recommend_candidates_for_job(job, all_candidates, limit)

        return render_template(
            "employer/recommendations.html",
            job=job,
            results=results,
            is_member=is_member,
            limit=limit,
        )