
"""
Handles creation of the employers table if it doesn't already exist
"""

class EmployersDatabase:
    """Manages the employers table."""

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

    def insert(self, data):
        """Inserts a new employer profile and returns the new row id."""

        #Direct dict access used on user_id and company_name to prevent Null being assigned if no data entered
        cursor = self.conn.execute(
            """INSERT INTO employers
               (user_id, company_name, company_description, industry, location,
                weburl, contact_email, source)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                data["user_id"],
                data["company_name"],
                data.get("company_description"),
                data.get("industry"),
                data.get("location"),
                data.get("weburl"),
                data.get("contact_email"),
                data.get("source", "registered")
            )
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_by_user_id(self, user_id):
        """Returns a single employer profile row as dict, or None if not found."""
        row = self.conn.execute(
            "SELECT * FROM employers WHERE user_id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None

    def count_by_source(self, source):
        """Returns the count of employer records matching the given source."""
        row = self.conn.execute(
            "SELECT COUNT(*) FROM employers WHERE source = ?", (source,)
        ).fetchone()
        return row[0]