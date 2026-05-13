
"""
Handles creation of the applications table if it doesn't already exist
"""

class ApplicationsDatabase:
    def __init__(self, conn):
        self.conn = conn
        self._create_table()
 
    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                job_listing_id INTEGER NOT NULL,
                job_seeker_id  INTEGER NOT NULL,
                cover_letter   TEXT,
                status         TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'reviewed', 'rejected', 'accepted')),
                applied_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_listing_id) REFERENCES job_listings(id),
                FOREIGN KEY (job_seeker_id)  REFERENCES job_seekers(id),
                UNIQUE (job_listing_id, job_seeker_id)
            );
        """)
        self.conn.commit()