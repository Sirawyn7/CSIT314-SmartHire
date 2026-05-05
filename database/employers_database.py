
"""
Handles creation of the employers table if it doesn't already exist
"""

class EmployerDatabase:
    def __init__(self, conn):
        self.conn = conn
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            );
        """)
        self.conn.commit()