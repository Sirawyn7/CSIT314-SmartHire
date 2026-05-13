
"""
Handles creation of the job_seekers table if it doesn't already exist
"""

class JobSeekersDatabase:
    def __init__(self, conn):
        self.conn = conn
        self._create_table()
 
    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS job_seekers (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL UNIQUE,
                full_name  TEXT NOT NULL,
                resume     TEXT,
                bio        TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        self.conn.commit()