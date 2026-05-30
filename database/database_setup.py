
"""
Opens the connection to the .db file, creating one if there isn't already
Sets connection level settings for the database and returned formatting
Provides functions to get the connection object for database classes and function to close the connection
"""

import sqlite3

class DatabaseSetup:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.row_factory = sqlite3.Row  # rows behave like dicts

    def get(self):
        return self.conn

    def close(self):
        self.conn.close()