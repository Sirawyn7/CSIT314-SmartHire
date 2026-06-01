

from core.users_core import User, Candidate, Employer
from database.seeders.seed_data.users_seed_data import SEED_USERS


class UsersSeeder:
    """Seeds initial user data for development."""

    def __init__(self, db):
        self.db = db
        self.seed()

    def seed(self):
        """Inserts seed users only if none already exist."""
        if self.db.candidates.count_by_source("seeded") > 0:
            return

        for data in SEED_USERS:
            user = self._build_user(data)
            self.db.users.insert(user)

    def _build_user(self, data):
        """Constructs the correct User subclass instance from raw seed data."""
        base = {
            "email": data["email"],
            "password_hash": User.hash_password(data["password"]),
            "user_type": data["user_type"],
            "is_member": data.get("is_member", 0),
        }

        if data["user_type"] == "candidate":
            profile = {
                "full_name": data["full_name"],
                "phone": data.get("phone"),
                "education": data.get("education"),
                "field_of_study": data.get("field_of_study"),
                "years_experience": data.get("years_experience", 0),
                "skills": data.get("skills"),
                "work_experience": data.get("work_experience"),
                "preferred_work_mode": data.get("preferred_work_mode"),
                "preferred_location": data.get("preferred_location"),
                "source": "seeded"
            }
            return Candidate(base, profile)

        elif data["user_type"] == "employer":
            profile = {
                "company_name": data["company_name"],
                "company_description": data.get("company_description"),
                "industry": data.get("industry"),
                "location": data.get("location"),
                "weburl": data.get("weburl"),
                "contact_email": data.get("contact_email"),
                "source": "seeded"
            }
            return Employer(base, profile)

        else:
            return User(base)