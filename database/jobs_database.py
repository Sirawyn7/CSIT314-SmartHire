
"""
Handles creation of the job listings table if it doesn't already exist
"""

class JobsDatabase:
    def __init__(self, conn):
        self.conn = conn
        self._create_table()
 
    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employer_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                required_education TEXT CHECK(required_education IN ('High School', 'Bachelor', 'Master', 'PhD')),
                required_skills TEXT,
                years_experience_required INTEGER DEFAULT 0,
                work_mode TEXT CHECK(work_mode IN ('Remote', 'On-site', 'Hybrid')),
                location TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employer_id) REFERENCES employers(id)
            )
        """)
        self.conn.commit()