
"""
Initialises tables in the correct order
Allows app.py to only import this file, with this handling instantiating the table classes in the 
correct order automatically
"""

from database.database_setup import DatabaseSetup
from database.users_database import UsersDatabase
from database.job_seekers_database import JobSeekersDatabase
from database.employers_database import EmployersDatabase
from database.job_listings_database import JobListingsDatabase
from database.applications_database import ApplicationsDatabase
 
 
class DatabaseManager:
    def __init__(self, db_path):
        self.connection = DatabaseSetup(db_path)
        conn = self.connection.get()
 
        # Order matters — tables with foreign keys must come after their dependencies
        self.users        = UsersDatabase(conn)
        self.job_seekers  = JobSeekersDatabase(conn)
        self.employers    = EmployersDatabase(conn)
        self.job_listings = JobListingsDatabase(conn)
        self.applications = ApplicationsDatabase(conn)
 
    def close(self):
        self.connection.close()