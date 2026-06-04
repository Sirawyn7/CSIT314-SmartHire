
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
    
    def get_recent_by_employer_id(self, employer_id, limit=4):
        """Returns the most recent job rows for an employer."""
        rows = self.conn.execute(
            """
            SELECT *
            FROM jobs
            WHERE employer_id = ?
            ORDER BY datetime(created_at) DESC, id DESC
            LIMIT ?
            """,
            (employer_id, limit)
        ).fetchall()
        return [dict(row) for row in rows]
    
    def get_all_active_paginated(self, page, per_page):
        """Returns active jobs with company name for a given page. Returns (list of dicts, total count)."""
        offset = (page - 1) * per_page
        rows = self.conn.execute(
            """
            SELECT jobs.*, employers.company_name
            FROM jobs
            JOIN employers ON jobs.employer_id = employers.id
            WHERE jobs.is_active = 1
            ORDER BY jobs.created_at DESC
            LIMIT ? OFFSET ?
            """,
            (per_page, offset)
        ).fetchall()
        total = self.conn.execute(
            "SELECT COUNT(*) FROM jobs WHERE is_active = 1"
        ).fetchone()[0]
        return [dict(row) for row in rows], total
    
    def get_by_id(self, job_id):
        """Returns a single active job with company name by job ID, or None if not found."""
        row = self.conn.execute(
            """
            SELECT jobs.*, employers.company_name
            FROM jobs
            JOIN employers ON jobs.employer_id = employers.id
            WHERE jobs.id = ?
            """,
            (job_id,)
        ).fetchone()
        return dict(row) if row else None
    
    def get_all_active_with_employer(self):
        """Returns all active jobs with company name as a list of dicts."""
        rows = self.conn.execute(
            """
            SELECT jobs.*, employers.company_name
            FROM jobs
            JOIN employers ON jobs.employer_id = employers.id
            WHERE jobs.is_active = 1
            ORDER BY jobs.created_at DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def get_all_unique_skills(self):
        """Returns a sorted list of unique skills extracted from all active job postings."""
        rows = self.conn.execute(
            "SELECT required_skills FROM jobs WHERE is_active = 1 AND required_skills IS NOT NULL"
        ).fetchall()
        skills = set()
        for row in rows:
            for skill in row["required_skills"].split(","):
                stripped = skill.strip()
                if stripped:
                    skills.add(stripped)
        return sorted(skills)
    
    def get_all_by_employer_id(self, employer_id):
        """Returns all jobs (active and inactive) for a given employer."""
        rows = self.conn.execute(
            """
            SELECT * FROM jobs
            WHERE employer_id = ?
            ORDER BY datetime(created_at) DESC, id DESC
            """,
            (employer_id,)
        ).fetchall()
        return [dict(row) for row in rows]

    def set_active_status(self, job_id, employer_id, status):
        """Sets is_active for a job, only if it belongs to the given employer."""
        self.conn.execute(
            """
            UPDATE jobs SET is_active = ?
            WHERE id = ? AND employer_id = ?
            """,
            (status, job_id, employer_id)
        )
        self.conn.commit()

    def update_by_id_and_employer_id(self, job_id, employer_id, data):
        """Updates a job only if it belongs to the given employer."""
        self.conn.execute(
            """
            UPDATE jobs
            SET
                title = ?,
                description = ?,
                required_education = ?,
                required_skills = ?,
                years_experience_required = ?,
                work_mode = ?,
                location = ?
            WHERE id = ? AND employer_id = ?
            """,
            (
                data.get("title"),
                data.get("description"),
                data.get("required_education"),
                data.get("required_skills"),
                data.get("years_experience_required"),
                data.get("work_mode"),
                data.get("location"),
                job_id,
                employer_id,
            )
        )
        self.conn.commit()