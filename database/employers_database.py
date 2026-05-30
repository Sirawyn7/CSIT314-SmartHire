
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                company_name TEXT NOT NULL,
                company_description TEXT,
                industry TEXT,
                location TEXT,
                weburl TEXT,
                contact_email TEXT,
                source TEXT DEFAULT 'registered',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()