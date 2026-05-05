
"""
Handles creation of the job_seekers table if it doesn't already exist
"""

class JobSeekerDatabase:
    def __init__(self, conn):
        self.conn = conn
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS job_seekers (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            );
        """)
        self.conn.commit()