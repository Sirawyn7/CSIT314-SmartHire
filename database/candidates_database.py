
"""
Handles creation of the job_seekers table if it doesn't already exist
"""

class CandidatesDatabase:
    """Manages the candidates table."""

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
    
    def insert(self, data):
        """Inserts a new candidate profile and returns the new row id."""

        #Direct dict access used on user_id and full_name to prevent Null being assigned if no data entered
        cursor = self.conn.execute(
            """INSERT INTO candidates 
               (user_id, full_name, phone, education, field_of_study, years_experience,
                skills, work_experience, preferred_work_mode, preferred_location, source)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                data["user_id"], 
                data["full_name"],
                data.get("phone"),
                data.get("education"),
                data.get("field_of_study"),
                data.get("years_experience", 0),
                data.get("skills"),
                data.get("work_experience"),
                data.get("preferred_work_mode"),
                data.get("preferred_location"),
                data.get("source", "registered")
            )
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_by_user_id(self, user_id):
        """Returns a single candidate profile row as dict, or None if not found."""
        row = self.conn.execute(
            "SELECT * FROM candidates WHERE user_id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None

    def count_by_source(self, source):
        """Returns the count of candidate records matching the given source."""
        row = self.conn.execute(
            "SELECT COUNT(*) FROM candidates WHERE source = ?", (source,)
        ).fetchone()
        return row[0]
    
    def update_by_user_id(self, user_id, data):
        """Updates a candidate profile by user_id."""
        years_experience = data.get("years_experience")
        if years_experience in (None, ""):
            years_experience = 0

        self.conn.execute(
            """
            UPDATE candidates
            SET
                full_name = ?,
                phone = ?,
                education = ?,
                field_of_study = ?,
                years_experience = ?,
                skills = ?,
                work_experience = ?,
                preferred_work_mode = ?,
                preferred_location = ?
            WHERE user_id = ?
            """,
            (
                data.get("full_name"),
                data.get("phone"),
                data.get("education"),
                data.get("field_of_study"),
                years_experience,
                data.get("skills"),
                data.get("work_experience"),
                data.get("preferred_work_mode"),
                data.get("preferred_location"),
                user_id,
            )
        )
        self.conn.commit()

    def get_all(self):
        """Returns all candidate rows as a list of dicts, including account email."""
        rows = self.conn.execute(
            """
            SELECT
                candidates.*,
                users.email AS email
            FROM candidates
            JOIN users
                ON users.id = candidates.user_id
            WHERE users.user_type = 'candidate'
            ORDER BY candidates.id ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]