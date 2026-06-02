
from core.jobs_core import Job
from database.seeders.seed_data.jobs_seed_data import JOBS
 
 
class JobSeeder:
    """Seeds initial job data for development."""
 
    def __init__(self, db):
        self.db = db
        self.seed()
 
    def seed(self):
        """Inserts seed jobs only if none already exist."""
        if self.db.jobs.count_by_source("seeded") > 0:
            return
 
        employers = self.db.employers.get_all()
        jobs = self._build_jobs(employers)
 
        for job in jobs:
            self.db.jobs.insert(job)
 
    def _build_jobs(self, employers):
        """
        Constructs a list of Job instances from seed data, distributed across employers.
        """
        num_employers = len(employers)
        num_jobs = len(JOBS)
 
        base_count = num_jobs // num_employers
        remainder = num_jobs % num_employers
 
        jobs = []
        job_index = 0
 
        for i, employer in enumerate(employers):
            count = base_count + (1 if i < remainder else 0)
 
            for job_data in JOBS[job_index:job_index + count]:
                data = dict(job_data)
                data["employer_id"] = employer["id"]
                data["source"] = "seeded"
                jobs.append(Job(data))
 
            job_index += count
 
        return jobs