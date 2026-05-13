
"""
Handles creation of the users table if it doesn't already exist
"""

class UsersDatabase:
    def __init__(self, conn):
        self.conn = conn
        self._create_table()
 
    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role          TEXT NOT NULL CHECK(role IN ('job_seeker', 'employer')),
                created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.conn.commit()