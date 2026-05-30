
"""
Initialises tables in the correct order
Allows app.py to only import this file, with this handling instantiating the table classes in the 
correct order automatically
"""

from database.database_setup import DatabaseSetup
from database.users_database import UsersDatabase
from database.candidates_database import CandidatesDatabase
from database.employers_database import EmployersDatabase
from database.jobs_database import JobsDatabase
from database.applications_database import ApplicationsDatabase
from database.members_database import MembersDatabase
 
 
class DatabaseManager:
    def __init__(self, db_path):
        self.connection = DatabaseSetup(db_path)
        conn = self.connection.get()
 
        # Order matters — tables with foreign keys must come after their dependencies
        self.users        = UsersDatabase(conn)
        self.candidates   = CandidatesDatabase(conn)
        self.employers    = EmployersDatabase(conn)
        self.jobs         = JobsDatabase(conn)
        self.applications = ApplicationsDatabase(conn)
        self.memberships  = MembersDatabase(conn)
    
    def close(self):
        self.connection.close()