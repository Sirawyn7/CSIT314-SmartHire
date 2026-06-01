
"""
Routes handle the routing of web requests, e.g. moving between webpages
Allows app.py to only import this file, packaging all routes together.
"""

from routes.auth_routes import AuthRoutes
from routes.candidate_routes import CandidateRoutes
from routes.employers_routes import EmployerRoutes
from routes.admin_routes import AdminRoutes

route_classes = [
    AuthRoutes,
    CandidateRoutes,
    EmployerRoutes,
    AdminRoutes
    ]