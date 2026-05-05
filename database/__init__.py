
"""
Initialises tables in the correct order
Allows app.py to only import this file, with this handling instantiating the table classes in the 
correct order automatically
"""

from database_setup import DatabaseSetup
from database.job_seelers_database import JobSeekerDatabase
from database.employers_database import EmployerDatabase



class DatabaseManager:
    def __init__(self, db_path):
        self.connection = DatabaseSetup(db_path)
        conn = self.connection.get()

        # Order matters — tables with foreign keys must come after their dependencies
        self.users     = JobSeekerDatabase(conn)
        self.users     = EmployerDatabase(conn)

    def close(self):
        self.connection.close()