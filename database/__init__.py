
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
from database.memberships_database import MembershipsDatabase
from database.payments_database import PaymentsDatabase
from database.seeders.users_seeder import UsersSeeder
from database.seeders.jobs_seeder import JobSeeder
 
 
class DatabaseManager:
    def __init__(self, db_path):
        self.connection = DatabaseSetup(db_path)
        conn = self.connection.get()

        self.candidates   = CandidatesDatabase(conn)
        self.employers    = EmployersDatabase(conn)
        self.users        = UsersDatabase(conn, self)
        self.jobs         = JobsDatabase(conn)
        self.applications = ApplicationsDatabase(conn)
        self.memberships  = MembershipsDatabase(conn)
        self.payments     = PaymentsDatabase(conn)

        self.users_seeder = UsersSeeder(self)
        self.job_seeder   = JobSeeder(self)

    def close(self):
        self.connection.close()