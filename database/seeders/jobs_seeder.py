
from core.jobs_core import Job
from database.seeders.seed_data.jobs_seed_data import JOB_PAIRS
 
 
class JobSeeder:
    """Seeds initial job data for development"""
 
    def __init__(self, db):
        self.db = db
        self.seed()
 
    def seed(self):
        """Inserts seed jobs only if none already exist"""
        if self.db.jobs.count_by_source("seeded") > 0:
            return
 
        employers = self.db.employers.get_all()
        jobs = self._build_jobs(employers)
 
        for job in jobs:
            self.db.jobs.insert(job)
 
    def _build_jobs(self, employers):
        """Constructs a list of Job instances from seed data, assigned to employers by index"""
        jobs = []
        for index, employer in enumerate(employers):
            first_data, second_data = JOB_PAIRS[index]
 
            first_data["employer_id"] = employer["id"]
            first_data["source"] = "seeded"
 
            second_data["employer_id"] = employer["id"]
            second_data["source"] = "seeded"
 
            jobs.append(Job(first_data))
            jobs.append(Job(second_data))
 
        return jobs