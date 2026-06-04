
"""
Routes handle the routing of web requests, e.g. moving between webpages
Allows app.py to only import this file, packaging all routes together.
"""

from routes.auth_routes import AuthRoutes
from routes.home_routes import HomeRoutes
from routes.candidate_routes import CandidateRoutes
from routes.employers_routes import EmployerRoutes
from routes.admin_routes import AdminRoutes
from routes.jobs_routes import JobRoutes
from routes.recommendations_routes import RecommendationRoutes
from routes.membership_routes import MembershipRoutes

route_classes = [
    AuthRoutes,
    HomeRoutes,
    CandidateRoutes,
    EmployerRoutes,
    AdminRoutes,
    JobRoutes,
    RecommendationRoutes,
    MembershipRoutes
    ]