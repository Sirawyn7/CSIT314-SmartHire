
"""
Handles creation of the job_seekers table if it doesn't already exist
"""

class CandidatesDatabase:
    def __init__(self, conn):
        self.conn = conn
        self._create_table()
 
    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                full_name TEXT NOT NULL,
                phone TEXT,
                education TEXT CHECK(education IN ('High School', 'Bachelor', 'Master', 'PhD')),
                field_of_study TEXT,
                years_experience INTEGER DEFAULT 0,
                skills TEXT,
                work_experience TEXT,
                preferred_work_mode TEXT CHECK(preferred_work_mode IN ('Remote', 'On-site', 'Hybrid')),
                preferred_location TEXT,
                source TEXT DEFAULT 'registered',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()