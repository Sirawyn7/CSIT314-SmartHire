
"""
Handles creation of the job listings table if it doesn't already exist
"""

class JobsDatabase:
    """Manages the jobs table."""
 
    def __init__(self, conn):
        self.conn = conn
        self._create_table()
 
    def _create_table(self):
        """Creates the jobs table if it does not already exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employer_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                required_education TEXT,
                required_skills TEXT,
                years_experience_required INTEGER,
                work_mode TEXT CHECK(work_mode IN ('Remote', 'On-site', 'Hybrid')),
                location TEXT,
                is_active INTEGER DEFAULT 1,
                source TEXT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employer_id) REFERENCES employers(id)
            )
        """)
        self.conn.commit()
 
    def insert(self, job):
        """Inserts a new job posting and returns the new row id."""
        cursor = self.conn.execute(
            """
            INSERT INTO jobs (
                employer_id,
                title,
                description,
                required_education,
                required_skills,
                years_experience_required,
                work_mode,
                location,
                is_active,
                source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job.employer_id,
                job.title,
                job.description,
                job.required_education,
                job.required_skills,
                job.years_experience_required,
                job.work_mode,
                job.location,
                job.is_active,
                job.source,
            )
        )
        self.conn.commit()
        return cursor.lastrowid
 
    def count_by_source(self, source):
        """Returns the number of job rows matching the given source value."""
        row = self.conn.execute(
            "SELECT COUNT(*) FROM jobs WHERE source = ?", (source,)
        ).fetchone()
        return row[0]