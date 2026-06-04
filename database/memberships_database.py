
"""
Handles creation of the members table if it doesn't already exist
"""

class MembershipsDatabase:
    """Manages the memberships table."""

    def __init__(self, conn):
        self.conn = conn
        self._create_table()

    def _create_table(self):
        """Creates the memberships table if it does not already exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memberships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()

    def insert(self, user_id, started_at=None):
        """Inserts a new membership row and returns the new row id."""
        if started_at is not None:
            cursor = self.conn.execute(
                "INSERT INTO memberships (user_id, started_at) VALUES (?, ?)",
                (user_id, started_at)
            )
        else:
            cursor = self.conn.execute(
                "INSERT INTO memberships (user_id) VALUES (?)",
                (user_id,)
            )
        self.conn.commit()
        return cursor.lastrowid

    def get_by_user_id(self, user_id):
        """Returns the most recent membership row for a user, or None if not found."""
        row = self.conn.execute(
            "SELECT * FROM memberships WHERE user_id = ? ORDER BY started_at DESC LIMIT 1",
            (user_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_all(self):
        """Returns all membership rows as a list of dicts."""
        rows = self.conn.execute(
            "SELECT * FROM memberships"
        ).fetchall()
        return [dict(row) for row in rows]
