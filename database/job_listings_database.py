
"""
Handles creation of the job listings table if it doesn't already exist
"""

class JobListingsDatabase:
    def __init__(self, conn):
        self.conn = conn
        self._create_table()
 
    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS job_listings (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                employer_id INTEGER NOT NULL,
                title       TEXT NOT NULL,
                location    TEXT,
                description TEXT NOT NULL,
                status      TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'closed')),
                posted_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employer_id) REFERENCES employers(id)
            );
        """)
        self.conn.commit()