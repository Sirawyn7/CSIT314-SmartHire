
"""
Handles creation of the users table if it doesn't already exist
"""

class UsersDatabase:
    """Manages the users table and orchestrates profile insertion for all user types."""

    def __init__(self, conn, db):
        self.conn = conn
        self.db = db    #Gains access to db instead of just conn as it needs to access candidate/employer tables
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

    def insert(self, user):
        """Inserts a user into the users table and delegates profile insertion based on user_type."""
        cursor = self.conn.execute(
            "INSERT INTO users (email, password_hash, user_type, is_member) VALUES (?, ?, ?, ?)",
            (user.email, user.password_hash, user.user_type, int(user.is_member))
        )
        self.conn.commit()
        user_id = cursor.lastrowid

        if user.user_type == "candidate":
            self.db.candidates.insert({
                "user_id": user_id,
                "full_name": user.full_name,
                "phone": user.phone,
                "education": user.education,
                "field_of_study": user.field_of_study,
                "years_experience": user.years_experience,
                "skills": user.skills,
                "work_experience": user.work_experience,
                "preferred_work_mode": user.preferred_work_mode,
                "preferred_location": user.preferred_location,
                "source": user.source
            })

        elif user.user_type == "employer":
            self.db.employers.insert({
                "user_id": user_id,
                "company_name": user.company_name,
                "company_description": user.company_description,
                "industry": user.industry,
                "location": user.location,
                "weburl": user.weburl,
                "contact_email": user.contact_email,
                "source": user.source
            })

    def get_by_user_id(self, user_id):
        """Returns a single user row as dict, or None if not found."""
        row = self.conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None
    
    def get_by_email(self, email):
        """Returns a user row as a dict matching the given email, or None if not found."""
        row = self.conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        return dict(row) if row else None

    def get_password_hash(self, user_id):
        """Returns the password_hash string for the given user_id, or None if not found."""
        row = self.conn.execute(
            "SELECT password_hash FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return row["password_hash"] if row else None
    
    def set_member_status(self, user_id, status):
        """Sets the is_member flag for a user to the given status (1 or 0)."""
        self.conn.execute(
            "UPDATE users SET is_member = ? WHERE id = ?",
            (status, user_id)
        )
        self.conn.commit()