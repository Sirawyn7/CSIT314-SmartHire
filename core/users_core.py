
"""
Candidates and Employers inherit from User parent class
A factory method is used for user type instantiation
"""


import bcrypt


class User:
    """Base class for all user types."""

    def __init__(self, data):
        self.email         = data["email"]
        self.password_hash = data["password_hash"]
        self.user_type     = data["user_type"]
        self.is_member     = bool(data["is_member"])

    @staticmethod
    def create(user_row, db):
        """Factory method — returns correct subclass instance based on user_type."""

        user_type = user_row["user_type"]

        if user_type == "candidate":
            profile = db.candidates.get_by_user_id(user_row["id"])
            return Candidate(user_row, profile)
        
        elif user_type == "employer":
            profile = db.employers.get_by_user_id(user_row["id"])
            return Employer(user_row, profile)
        
        else:
            return User(user_row)   #admin - no extended profile

    @staticmethod
    def hash_password(password):
        """Returns a bcrypt hash of the given password string."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        """Returns True if the given password matches the stored bcrypt hash."""
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())


class Candidate(User):
    """Candidate user with extended profile data."""

    def __init__(self, user_data, profile_data):
        super().__init__(user_data)
        self.full_name              = profile_data["full_name"]
        self.phone                  = profile_data["phone"]
        self.education              = profile_data["education"]
        self.field_of_study         = profile_data["field_of_study"]
        self.years_experience       = profile_data["years_experience"]
        self.skills                 = profile_data["skills"]
        self.work_experience        = profile_data["work_experience"]
        self.preferred_work_mode    = profile_data["preferred_work_mode"]
        self.preferred_location     = profile_data["preferred_location"]
        self.source                 = profile_data["source"]


class Employer(User):
    """Employer user with extended company profile data."""

    def __init__(self, user_data, profile_data):
        super().__init__(user_data)
        self.company_name           = profile_data["company_name"]
        self.company_description    = profile_data["company_description"]
        self.industry               = profile_data["industry"]
        self.location               = profile_data["location"]
        self.weburl                 = profile_data["weburl"]
        self.contact_email          = profile_data["contact_email"]
        self.source                 = profile_data["source"]