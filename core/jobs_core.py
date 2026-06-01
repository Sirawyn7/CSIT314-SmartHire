

class Job:
    """Represents a job posting"""
 
    def __init__(self, data):
        self.employer_id              = data["employer_id"]
        self.title                    = data["title"]
        self.description              = data["description"]
        self.required_education       = data.get("required_education")
        self.required_skills          = data.get("required_skills")
        self.years_experience_required = data.get("years_experience_required")
        self.work_mode                = data.get("work_mode")
        self.location                 = data.get("location")
        self.is_active                = data.get("is_active", 1)
        self.source                   = data.get("source")