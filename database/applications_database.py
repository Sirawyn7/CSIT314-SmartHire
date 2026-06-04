"""
Handles creation and management of the applications table.
"""


class ApplicationsDatabase:
    """Manages candidate job applications."""

    def __init__(self, conn):
        self.conn = conn
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                candidate_id INTEGER NOT NULL,
                cover_letter TEXT,
                status TEXT NOT NULL DEFAULT 'pending'
                    CHECK(status IN ('pending', 'reviewed', 'contacted', 'rejected', 'accepted', 'withdrawn')),
                applied_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs(id),
                FOREIGN KEY (candidate_id) REFERENCES candidates(id),
                UNIQUE (job_id, candidate_id)
            );
            """
        )
        self.conn.commit()

    def get_by_candidate_and_job(self, candidate_id, job_id):
        row = self.conn.execute(
            """
            SELECT *
            FROM applications
            WHERE candidate_id = ? AND job_id = ?
            """,
            (candidate_id, job_id),
        ).fetchone()
        return dict(row) if row else None

    def create(self, candidate_id, job_id, cover_letter=None):
        cursor = self.conn.execute(
            """
            INSERT INTO applications (job_id, candidate_id, cover_letter)
            VALUES (?, ?, ?)
            """,
            (job_id, candidate_id, cover_letter),
        )
        self.conn.commit()
        return cursor.lastrowid

    def update_cover_letter(self, application_id, cover_letter=None):
        self.conn.execute(
            """
            UPDATE applications
            SET cover_letter = ?
            WHERE id = ?
            """,
            (cover_letter, application_id),
        )
        self.conn.commit()

    def create_or_update(self, candidate_id, job_id, cover_letter=None):
        existing = self.get_by_candidate_and_job(candidate_id, job_id)

        if existing:
            self.conn.execute(
                """
                UPDATE applications
                SET cover_letter = ?, status = 'pending'
                WHERE id = ?
                """,
                (cover_letter, existing["id"]),
            )
            self.conn.commit()
            return self.get_by_candidate_and_job(candidate_id, job_id), False

        self.create(candidate_id, job_id, cover_letter)
        return self.get_by_candidate_and_job(candidate_id, job_id), True
    
    def get_all_by_candidate_id(self, candidate_id):
        """Returns all applications for a candidate with related job and employer details."""
        rows = self.conn.execute(
            """
            SELECT
                applications.*,
                jobs.title,
                jobs.location,
                jobs.work_mode,
                jobs.is_active,
                employers.company_name
            FROM applications
            JOIN jobs ON applications.job_id = jobs.id
            JOIN employers ON jobs.employer_id = employers.id
            WHERE applications.candidate_id = ?
            ORDER BY datetime(applications.applied_at) DESC, applications.id DESC
            """,
            (candidate_id,),
        ).fetchall()
        return [dict(row) for row in rows]
    
    
    def update_status_by_id_and_candidate_id(self, application_id, candidate_id, status):
        """Updates an application status only if it belongs to the given candidate."""
        self.conn.execute(
            """
            UPDATE applications
            SET status = ?
            WHERE id = ? AND candidate_id = ?
            """,
            (status, application_id, candidate_id),
        )
        self.conn.commit()

    def get_all_by_job_id_and_employer_id(self, job_id, employer_id):
        rows = self.conn.execute(
            """
            SELECT
                applications.*,
                candidates.full_name,
                candidates.phone,
                candidates.education,
                candidates.field_of_study,
                candidates.years_experience,
                candidates.skills,
                candidates.work_experience,
                candidates.preferred_work_mode,
                candidates.preferred_location,
                users.email,
                jobs.title AS job_title,
                jobs.required_education,
                jobs.required_skills,
                jobs.years_experience_required,
                jobs.work_mode AS job_work_mode,
                jobs.location AS job_location,
                jobs.description AS job_description
            FROM applications
            JOIN jobs ON applications.job_id = jobs.id
            JOIN candidates ON applications.candidate_id = candidates.id
            JOIN users ON candidates.user_id = users.id
            WHERE applications.job_id = ?
            AND jobs.employer_id = ?
            ORDER BY datetime(applications.applied_at) DESC, applications.id DESC
            """,
            (job_id, employer_id),
        ).fetchall()
        return [dict(row) for row in rows]

    def update_status_by_id_and_employer_id(self, application_id, employer_id, status):
        row = self.conn.execute(
            """
            SELECT applications.job_id
            FROM applications
            JOIN jobs ON applications.job_id = jobs.id
            WHERE applications.id = ?
            AND jobs.employer_id = ?
            """,
            (application_id, employer_id),
        ).fetchone()

        if not row:
            return None

        self.conn.execute(
            """
            UPDATE applications
            SET status = ?
            WHERE id = ?
            """,
            (status, application_id),
        )
        self.conn.commit()
        return row["job_id"]
    
    def get_accepted_job_ids_by_candidate_id(self, candidate_id):
        rows = self.conn.execute(
            """
            SELECT job_id
            FROM applications
            WHERE candidate_id = ? AND status = 'accepted'
            """,
            (candidate_id,),
        ).fetchall()
        return [row["job_id"] for row in rows]