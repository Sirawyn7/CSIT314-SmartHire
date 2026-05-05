
"""
Routes handle the routing of web requests, e.g. moving between webpages
Allows app.py to only import this file, packaging all routes together.
"""

from routes.auth import auth_bp

blueprints = [auth_bp]