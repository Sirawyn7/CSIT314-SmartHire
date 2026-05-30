
"""
Handles creation of the users table if it doesn't already exist
"""

class UsersDatabase:
    def __init__(self, conn):
        self.conn = conn
        self._create_table()
 
    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                user_type TEXT NOT NULL CHECK(user_type IN ('candidate', 'employer', 'admin')),
                is_member INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()