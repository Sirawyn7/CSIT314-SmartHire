
"""
Handles creation of the employers table if it doesn't already exist
"""

class EmployersDatabase:
    def __init__(self, conn):
        self.conn = conn
        self._create_table()
 
    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER NOT NULL UNIQUE,
                company_name TEXT NOT NULL,
                website      TEXT,
                description  TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        self.conn.commit()