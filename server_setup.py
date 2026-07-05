
"""
Flask Server Class
"""

from flask import Flask, jsonify
import webbrowser
import os
from apscheduler.schedulers.background import BackgroundScheduler
from database import DatabaseManager
from routes import route_classes
from config import SECRET_KEY, MEMBERSHIP_CHECK_HOUR
from core.membership_core import MembershipManager

#-----------
class Server:

    #Singleton design principle used to ensure that only 1 server is ever created at a time
    _instance = None

    def __new__(cls, db_path):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialised = False
        return cls._instance

    def __init__(self, db_path):
        if self._initialised:
            return
        
        self.app = Flask(
            __name__,
            template_folder="web/templates",
            static_folder="web/static"
        )
        self.db = DatabaseManager(db_path)
        self._register_routes()
        self._start_scheduler()
        self._initialised = True
        self.app.secret_key = SECRET_KEY

    def _register_routes(self):
        #Register debug function
        self.app.add_url_rule("/ping", view_func=self.ping, methods=["GET"])

        #Register remaining functions
        for route_class in route_classes:
            instance = route_class(self.db)
            self.app.register_blueprint(instance.blueprint)

    def _start_scheduler(self):
        """Initialises and starts the background scheduler for overnight membership checks."""
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=self._run_membership_check, trigger="cron", hour=MEMBERSHIP_CHECK_HOUR)
        scheduler.start()

    def _run_membership_check(self):
        """Runs the overnight membership lapse check. Called by the scheduler at the configured hour."""
        manager = MembershipManager(self.db)
        manager.lapse_overdue_memberships()

    #Debug function
    def ping(self):
        return jsonify({"message": "Server is running"}), 200

    def run(self):
        #Debug mode runs test launch, this ensures webpage is only opened on main launch
        if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
            webbrowser.open("http://127.0.0.1:5000/home")
        self.app.run(debug=True)
