

from config import (SKILL_WEIGHT, EXPERIENCE_WEIGHT, EDUCATION_WEIGHT, WORK_MODE_WEIGHT, LOCATION_WEIGHT, EDUCATION_LEVELS,)

class Matcher:
    """Recommendation engine — scores candidate/job pairs and returns ranked results.
    
    All scoring operates on raw database row dicts — no object construction.
    """

    def recommend_jobs_for_candidate(self, candidate, all_jobs, limit):
        """Returns a sorted list of (job_dict, score) tuples for a given candidate dict.

        Sorted by score descending, ties broken by job id ascending.
        limit is None for unlimited (members) or an integer cap (non-members).
        """
        scored = [
            (job, self._score_candidate_job(candidate, job))
            for job in all_jobs
        ]
        scored.sort(key=lambda x: (-x[1], x[0]["id"]))
        if limit is not None:
            scored = scored[:limit]
        return [(job, round(score * 100)) for job, score in scored]

    def recommend_candidates_for_job(self, job, all_candidates, limit):
        """Returns a sorted list of (candidate_dict, score) tuples for a given job dict.

        Sorted by score descending, ties broken by candidate id ascending.
        limit is None for unlimited (members) or an integer cap (non-members).
        """
        scored = [
            (candidate, self._score_candidate_job(candidate, job))
            for candidate in all_candidates
        ]
        scored.sort(key=lambda x: (-x[1], x[0]["id"]))
        if limit is not None:
            scored = scored[:limit]
        return [(candidate, round(score * 100)) for candidate, score in scored]

    def _score_candidate_job(self, candidate, job):
        """Returns a float 0–1 representing how well a candidate matches a job."""
        score = 0.0
        score += self._score_skills(candidate, job)      * SKILL_WEIGHT
        score += self._score_experience(candidate, job)  * EXPERIENCE_WEIGHT
        score += self._score_education(candidate, job)   * EDUCATION_WEIGHT
        score += self._score_work_mode(candidate, job)   * WORK_MODE_WEIGHT
        score += self._score_location(candidate, job)    * LOCATION_WEIGHT
        return score

    def _score_skills(self, candidate, job):
        """Returns proportion of required job skills present in candidate skills."""
        candidate_skills = self._parse_skills(candidate.get("skills", ""))
        job_skills = self._parse_skills(job.get("required_skills", ""))
        if not job_skills:
            return 1.0
        if not candidate_skills:
            return 0.0
        matched = candidate_skills.intersection(job_skills)
        return len(matched) / len(job_skills)

    def _score_experience(self, candidate, job):
        """Returns 1.0 if candidate meets or exceeds required experience, scaled otherwise."""
        candidate_years = candidate.get("years_experience") or 0
        required_years  = job.get("years_experience_required") or 0
        if required_years == 0:
            return 1.0
        if candidate_years >= required_years:
            return 1.0
        return candidate_years / required_years

    def _score_education(self, candidate, job):
        """Returns 1.0 if candidate education meets or exceeds the job requirement."""
        candidate_edu = candidate.get("education") or ""
        required_edu  = job.get("required_education") or ""
        if not required_edu:
            return 1.0
        levels = list(EDUCATION_LEVELS)
        candidate_level = levels.index(candidate_edu) if candidate_edu in levels else -1
        required_level  = levels.index(required_edu)  if required_edu  in levels else -1
        if required_level == -1:
            return 1.0
        if candidate_level == -1:
            return 0.0
        return 1.0 if candidate_level >= required_level else 0.0

    def _score_work_mode(self, candidate, job):
        """Returns 1.0 if candidate work mode preference matches the job, 0.0 otherwise."""
        candidate_mode = candidate.get("preferred_work_mode") or ""
        job_mode       = job.get("work_mode") or ""
        if not job_mode or not candidate_mode:
            return 1.0
        return 1.0 if candidate_mode.lower() == job_mode.lower() else 0.0

    def _score_location(self, candidate, job):
        """Returns 1.0 if candidate preferred location matches job location."""
        candidate_location = candidate.get("preferred_location") or ""
        job_location       = job.get("location") or ""
        if not job_location or not candidate_location:
            return 1.0
        return 1.0 if candidate_location.lower() in job_location.lower() else 0.0

    def _parse_skills(self, skills_str):
        """Parses a comma-separated skills string into a lowercase set."""
        if not skills_str:
            return set()
        return {s.strip().lower() for s in skills_str.split(",") if s.strip()}