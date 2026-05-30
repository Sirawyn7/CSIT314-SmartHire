
"""
Handles creation of the users table if it doesn't already exist
"""

class UsersDatabase:
    """Manages the users table."""

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

    def insert(self, data):
        """Inserts a new user and returns the new row id."""
        cursor = self.conn.execute(
            "INSERT INTO users (email, password_hash, user_type) VALUES (?, ?, ?)",
            (data["email"], data["password_hash"], data["user_type"])
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_by_user_id(self, user_id):
        """Returns a single user row as dict, or None if not found."""
        row = self.conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None