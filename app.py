
"""
Handles Initalisation of server
"""

from server_setup import Server

if __name__ == "__main__":
    server = Server(db_path="SmartHire.db")
    server.run()