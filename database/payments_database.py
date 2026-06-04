

class PaymentsDatabase:
    """Manages the payments table."""

    def __init__(self, conn):
        self.conn = conn
        self._create_table()

    def _create_table(self):
        """Creates the payments table if it does not already exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                period TEXT NOT NULL,
                paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()

    def insert(self, user_id, amount, period):
        """Inserts a new payment record and returns the new row id."""
        cursor = self.conn.execute(
            "INSERT INTO payments (user_id, amount, period) VALUES (?, ?, ?)",
            (user_id, amount, period)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_by_user_and_period(self, user_id, period):
        """Returns the payment for a given user and billing period, or None if not found."""
        row = self.conn.execute(
            "SELECT * FROM payments WHERE user_id = ? AND period = ?",
            (user_id, period)
        ).fetchone()
        return dict(row) if row else None

    def get_all_by_user_id(self, user_id):
        """Returns all payment records for a user as a list of dicts, most recent first."""
        rows = self.conn.execute(
            "SELECT * FROM payments WHERE user_id = ? ORDER BY paid_at DESC",
            (user_id,)
        ).fetchall()
        return [dict(row) for row in rows]